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
DSA=( "monrovia_basic" "monrovia_landuse" "monrovia_medicalcenters" "monrovia_schools" "monrovia_inlandwaters")
for DS in "${DSA[@]}"
do
   python  $BIN/cybergis-script-geogig-osm-sync.py true -v -gs $GS -ws $WS -ds $DS --username $USER --password $PASS -an $AN -ae $AE -to $TO
done
#===================#
DSA=( "kenema_basic" "kenema_landuse" "kenema_medicalcenters" "kenema_schools" "kenema_inlandwaters")
for DS in "${DSA[@]}"
do
   python $BIN/cybergis-script-geogig-osm-sync.py true -v -gs $GS -ws $WS -ds $DS --username $USER --password $PASS -an $AN -ae $AE -to $TO
done
#===================#
echo "Done updating OSM extracts."
