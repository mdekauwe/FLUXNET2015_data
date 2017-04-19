#!/usr/bin/env python
"""
Quick script to read in a FLUXNET 2015 file

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (19.04.2017)"
__email__ = "mdekauwe@gmail.com"

import matplotlib.pyplot as plt
import os
import sys
import glob
import pandas as pd


def read_flux_file(fname):

    date_parse = lambda x: pd.datetime.strptime(x, '%Y%m%d%H%M')
    df = pd.read_csv(fname, parse_dates=['TIMESTAMP_START'],
                     date_parser=date_parse)
    df = df.rename(columns={'TIMESTAMP_START': 'date'})
    df = df.drop('TIMESTAMP_END', 1)
    df = df.set_index('date')
    df['year'] = df.index.year
    df['doy'] = df.index.dayofyear
    df['hod'] = df.index.hour

    return (df)

if __name__ == "__main__":

    site = "AU-Tum"
    fdir = "data/raw_data/fluxnet2015_tier_1"
    fname = "FLX_%s_FLUXNET2015_FULLSET_HR_*.csv" % (site)
    fname = glob.glob(os.path.join(fdir, fname))[0]

    df = read_flux_file(fname)
    print(df)
