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

def get_site_info(site):

    fdir = "ancillary"
    fname = "FLX_AA-Flx_BIF_LATEST.xlsx"

    xls_file = pd.ExcelFile(os.path.join(fdir, fname))
    df = xls_file.parse('FLX-BIF')
    df = df.drop('GROUP_ID', 1)
    df = df.drop('VARIABLE_GROUP', 1)

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

    return (d)

def get_missing_elevation(lat, lon):
    """ If the elevation is missing get it from the gtopo30 data """

    url = ("http://api.geonames.org/gtopo30JSON?"
           "lat=%f&lng=%f&username=mdekauwe" % (lat, lon))
    r = requests.get(url)
    elev = r.json()['gtopo30']

    return elev
    
if __name__ == "__main__":

    site = "AU-Tum"
    d = get_site_info(site)
    print(d)

    site = "US-Ha1"
    d = get_site_info(site)
    print(d)
