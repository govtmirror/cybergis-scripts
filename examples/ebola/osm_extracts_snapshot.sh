#!/bin/bash
#==#
TIMESTAMP=$(date +%s)
#==#
WFS='http://example.com:8080/geoserver/wfs'
HOST='<Database Host>'
DB=<Database Name>
USER='postgres'
PASS=<Database Password>
NS=osm-extracts
PRJ='EPSG:4326'
#===================#
FTA=( "monrovia_basic_osm_buildings" "kenema_basic_osm_buildings" )
for FT in "${FTA[@]}"
do
    cybergis-script-pull-wfs.sh $WFS $NS $FT $PRJ $HOST $DB $USER $PASS $NS"_"$FT"_"$TIMESTAMP
done
