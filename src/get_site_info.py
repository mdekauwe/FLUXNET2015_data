#!/usr/bin/env python
"""
Get the site info from the FLUXNET2015 ancillary file

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (19.04.2017)"
__email__ = "mdekauwe@gmail.com"

import os
import pandas as pd
import requests
import subprocess
import numpy as np

def get_site_info(site, df):

    # We need to match our site and then extract the info we need. The data
    # is organised in a weird fashion, so need to account for that. Let's
    # return something nicer
    df = df[df.SITE_ID == site]
    d = {}
    d['site'] = site
    keys = ["COUNTRY", "IGBP", "LOCATION_LAT", "LOCATION_LONG", \
            "MAT", "MAP", "LOCATION_ELEV"]
    for i in keys:
        try:
            nvals = df[df["VARIABLE"] == i].DATAVALUE
            if len(nvals) > 1:
                x = df[df["VARIABLE"] == i].DATAVALUE.values
                d[i] = np.mean(x.astype(np.float))
            elif len(nvals) == 0:
                # Some sites have multiple lat/lon values, need to catch that
                x = df[df["VARIABLE"] == "LOCATION_LAT"].DATAVALUE.values
                lat = np.mean(x.astype(np.float))
                x = df[df["VARIABLE"] == "LOCATION_LONG"].DATAVALUE.values
                lon = np.mean(x.astype(np.float))
                elev = get_missing_elevation(float(lat), float(lon))
                d[i] = elev
            else:
                d[i] = df[df["VARIABLE"] == i].DATAVALUE.item()
        except ValueError:
            if i == "LOCATION_ELEV":
                lat = df[df["VARIABLE"] == "LOCATION_LAT"].DATAVALUE.item()
                lon = df[df["VARIABLE"] == "LOCATION_LONG"].DATAVALUE.item()
                elev = get_missing_elevation(float(lat), float(lon))
                d[i] = elev
            else:
                d[i] = -9999.9

    # clean up names
    d['country'] = d.pop('COUNTRY')
    d['pft'] = d.pop('IGBP')
    d['lat'] = d.pop('LOCATION_LAT')
    d['lon'] = d.pop('LOCATION_LONG')
    d['mat'] = d.pop('MAT')
    d['map'] = d.pop('MAP')
    d['elev'] = d.pop('LOCATION_ELEV')

    """
    # This is really slow as we scrape the website from scratch for each site,
    # it also fails, so you get error messages for sites with missing info.
    # Likely a neater way to do this, perhaps I will return to this later.
    try:
        tower_ht = subprocess.check_output(["Rscript",
                                            "src/get_missing_tower_height.R",
                                            site])
        tower_ht = tower_ht.decode("utf-8")
        if tower_ht != "NA\n":
            d['ht'] = float(tower_ht)
        else:
            d['ht'] = -9999.9
    except:
        d['ht'] = -9999.9
    """
    return (d)


def get_missing_elevation(lat, lon):
    """ If the elevation is missing get it from the gtopo30 data """

    url = ("http://api.geonames.org/gtopo30JSON?"
           "lat=%f&lng=%f&username=mdekauwe" % (lat, lon))
    r = requests.get(url)
    elev = r.json()['gtopo30']

    return elev

if __name__ == "__main__":

    fdir = "site_data"
    #fname = "FLX_AA-Flx_BIF_LATEST.csv"
    #df = pd.read_csv(os.path.join(fdir, fname), encoding='ISO-8859-1')
    fname = "FLX_AA-Flx_BIF_LATEST.xlsx"
    xls_file = pd.ExcelFile(os.path.join(fdir, fname))
    df = xls_file.parse('FLX-BIF')

    df = df.drop('GROUP_ID', 1)
    df = df.drop('VARIABLE_GROUP', 1)


    sites = np.unique(df.SITE_ID)
    print("site,country,pft,lat,lon,mat,map,elev")
    for site in sites:
        d = get_site_info(site, df)
        print("%s,%s,%s,%f,%f,%f,%f,%f" % (site, d['country'], d['pft'],
                                            float(d['lat']), float(d['lon']),
                                            float(d['mat']), float(d['map']),
                                            float(d['elev'])))
