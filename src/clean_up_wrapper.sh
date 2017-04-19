#!/bin/bash
#
# Get rid of files from the full archive we don't need for now to save some
# space, we can always go back to the original zips if we need to.
#
# Martin De Kauwe, 19 APR 2017
#
FLUX_ZIP_DIR=raw_data_tier_1_zip
FLUX_DIR=raw_data_tier_1

if [ ! -d $FLUX_DIR ]
then
    mkdir $FLUX_DIR
    cp $FLUX_ZIP_DIR/*.zip $FLUX_DIR/.
fi

# Unpack all the zip files and get rid of them for space reasons
for i in $FLUX_DIR/*.zip
do
    unzip $i
    rm $i
done

# Remove all the ERAI: Auxiliary data product containing full record
# (1989-2014) of downscaled micrometeorological variables
# (as related to the site’s measured variables) using the ERA-Interim
#reanalysis data product

for i in $FLUX_DIR/*_ERAI_*.csv
do
    rm $i
done

# Remove all the AUXMETEO files for space reasons, we don't want to keep the
# the ERA-Interim reanalysis data product

for i in $FLUX_DIR/*_AUXMETEO_*.csv
do
    rm $i
done

# Remove all the AUXNEE files for space reasons
for i in $FLUX_DIR/*_AUXNEE_*.csv
do
    rm $i
done
