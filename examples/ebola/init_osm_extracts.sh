#!/bin/bash
#==========##========#
USER=admin
PASS=geoserver
GS='http://localhost:8080/geoserver/'
WS=hiu
AN=hiu
AE='HIU_INFO@state.gov'
TO=180
RB=/home/ubuntu/statedep_geogig_demo/repos/
#===================#
#Monrovia - Basic
RN=monrovia_basic
REPO=$RB$RN
EXTENT='liberia:monrovia' 
MAPPING='basic:buildings_and_roads'
rm -fr $REPO
python /opt/cybergis-scripts.git/lib/rogue/geogig_init_extract.py  -v --path $REPO --name $RN --username $USER --password $PASS -gs $GS -ws $WS -to $TO --extent $EXTENT --mapping $MAPPING -an $AN -ae $AE
#===================#
#Monrovia - Landuse
RN=monrovia_landuse
REPO=$RB$RN
EXTENT='liberia:monrovia' 
MAPPING='landuse:landuse_all'
rm -fr $REPO
python /opt/cybergis-scripts.git/lib/rogue/geogig_init_extract.py  -v --path $REPO --name $RN --username $USER --password $PASS -gs $GS -ws $WS -to $TO --extent $EXTENT --mapping $MAPPING -an $AN -ae $AE
#===================#
#Monrovia - Medical Centers
RN=kenema_medicalcenters
REPO=$RB$RN
EXTENT='sierra_leone:kenema'
MAPPING='health:medical_centers'
rm -fr $REPO
python /opt/cybergis-scripts.git/lib/rogue/geogig_init_extract.py  -v --path $REPO --name $RN --username $USER --password $PASS -gs $GS -ws $WS -to $TO --extent $EXTENT --mapping $MAPPING -an $AN -ae $AE
#===================#
#Kenema - Basic
RN=kenema_basic
REPO=$RB$RN
EXTENT='sierra_leone:kenema'
MAPPING='basic:buildings_and_roads'
rm -fr $REPO
python /opt/cybergis-scripts.git/lib/rogue/geogig_init_extract.py  -v --path $REPO --name $RN --username $USER --password $PASS -gs $GS -ws $WS -to $TO --extent $EXTENT --mapping $MAPPING -an $AN -ae $AE
#===================#
#Kenema - Landuse
RN=kenema_landuse
REPO=$RB$RN
EXTENT='sierra_leone:kenema'
MAPPING='landuse:landuse_all'
rm -fr $REPO
python /opt/cybergis-scripts.git/lib/rogue/geogig_init_extract.py  -v --path $REPO --name $RN --username $USER --password $PASS -gs $GS -ws $WS -to $TO --extent $EXTENT --mapping $MAPPING -an $AN -ae $AE
#===================#
#Kenema - Medical Centers
RN=kenema_medicalcenters
REPO=$RB$RN
EXTENT='sierra_leone:kenema'
MAPPING='health:medical_centers'
rm -fr $REPO
python /opt/cybergis-scripts.git/lib/rogue/geogig_init_extract.py  -v --path $REPO --name $RN --username $USER --password $PASS -gs $GS -ws $WS -to $TO --extent $EXTENT --mapping $MAPPING -an $AN -ae $AE
