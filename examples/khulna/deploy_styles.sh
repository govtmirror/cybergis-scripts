#!/bin/bash
USER=admin
PASS=geoserver
GS='http://localhost:8080/geoserver/'
PRE=cybergis_
python /opt/cybergis-scripts.git/bin/cybergis-script-geoserver-import-styles.py  -v --path /opt/cybergis-styles.git/styles --username $USER --password $PASS -gs $GS --prefix $PRE
