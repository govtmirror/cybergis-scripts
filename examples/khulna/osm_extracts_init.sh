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
RB=/home/ubuntu/statedep_geogig_demo/repos/
#===================#
#Khulna
EXTENT='bangladesh:khulna'
#----------#
#Khulna - Basic
RN=khulna_basic
REPO=$RB$RN
MAPPING='basic:buildings_and_roads'
rm -fr $REPO
python $BIN/cybergis-script-geogig-osm-init.py  -v --path $REPO --name $RN --username $USER --password $PASS -gs $GS -ws $WS -to $TO --extent $EXTENT --mapping $MAPPING -an $AN -ae $AE
#===================#
#Khulna - Landuse
RN=khulna_landuse
REPO=$RB$RN
MAPPING='landuse:landuse_all'
rm -fr $REPO
python $BIN/cybergis-script-geogig-osm-init.py  -v --path $REPO --name $RN --username $USER --password $PASS -gs $GS -ws $WS -to $TO --extent $EXTENT --mapping $MAPPING -an $AN -ae $AE
#===================#
#Khulna - Medical Centers
RN=khulna_medicalcenters
REPO=$RB$RN
MAPPING='health:medical_centers'
rm -fr $REPO
python $BIN/cybergis-script-geogig-osm-init.py  -v --path $REPO --name $RN --username $USER --password $PASS -gs $GS -ws $WS -to $TO --extent $EXTENT --mapping $MAPPING -an $AN -ae $AE
#===================#
#Khulna - Schools
RN=khulna_schools
REPO=$RB$RN
MAPPING='education:schools'
rm -fr $REPO
python $BIN/cybergis-script-geogig-osm-init.py  -v --path $REPO --name $RN --username $USER --password $PASS -gs $GS -ws $WS -to $TO --extent $EXTENT --mapping $MAPPING -an $AN -ae $AE
#===================#
#Khulna - Inland Waters
RN=khulna_inlandwaters
REPO=$RB$RN
MAPPING='inlandWaters:inland_waters'
rm -fr $REPO
python /opt/cybergis-scripts.git/lib/rogue/geogig_init_extract.py  -v --path $REPO --name $RN --username $USER --password $PASS -gs $GS -ws $WS -to $TO --extent $EXTENT --mapping $MAPPING -an $AN -ae $AE
#===================#
