# FLUXNET2015_data

## Overview ##

FLUXNET data repository, including scripts to get rid of the files we don't
need. NB. we are working with the full set here.

## Datasets

* Eddy covariance dataset: [FLUXNET](http://fluxnet.fluxdata.org/data/fluxnet2015-dataset/)
* Elevation data: [GTOPO30](http://www.geonames.org/export/ws-overview.html)


## Instructions

To remove the stuff we don't want ...

```
$ src/clean_up_wrapper.sh
```

Couple of example scripts

```
$ python src/read_flux_file.py
$ python src/get_site_info.py 
```


## Contacts

- Martin De Kauwe: mdekauwe at gmail.com
