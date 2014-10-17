#!/bin/bash
#==========##========#
BIN=/opt/cybergis-scripts.git/bin
USER=admin
PASS=geoserver
GS='http://localhost:8080/geoserver/'
WS=osm-extracts
AN=hiu
AE='HIU_INFO@state.gov'
TO=360
#===================#
python  $BIN/cybergis-script-geogig-osm-sync.py false -v -gs $GS -ws $WS --username $USER --password $PASS -an $AN -ae $AE -to $TO --extracts osm_extracts.tsv
