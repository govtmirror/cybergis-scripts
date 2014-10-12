#!/bin/bash
#==========##========#
BIN=/opt/cybergis-scripts.git/bin
TIMESTAMP=$(date +%s)
#==#
USER=admin
PASS=geoserver
#==#
GS='http://localhost:8080/geoserver/'
#==#
WFS=$GS"wfs"
HOST='<Database Host>'
DB=<Database Name>
USER='postgres'
PASS=<Database Password>
NS=osm-extracts
PRJ='EPSG:4326'
#==#
#For publishing
WS=<Workspace>
DS=<Data Store>
#===================#
FTA=( "monrovia_basic_osm_buildings" "kenema_basic_osm_buildings")
for FT in "${FTA[@]}"
do
    SNAP=$NS"_"$FT"_"$TIMESTAMP
    echo "-----------"
    echo "Snapshoting "$FT" as "$NS"_"$FT"_"$TIMESTAMP
    echo "Snapshoting"
    $BIN/cybergis-script-pull-wfs.sh $WFS $NS $FT $PRJ $HOST $DB $USER $PASS $SNAP
    echo "Publishing"
    python $BIN/cybergis-script-geoserver-publish-layers.py -gs $GS -ws $WS -ds $DS -ft $SNAP --username $USER --password $PASS
done
#===================#
