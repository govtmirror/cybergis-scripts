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
#Monrovia
LG=monrovia_$TIMESTAMP
FTA=( "monrovia_basic_osm_buildings" "monrovia_basic_osm_roads")
SNAPA=()
STYLESA= ( "cybergis_structure_buildings" "cybergis_roads_roads_minor")
for FT in "${FTA[@]}"
do
    #SNAP=$NS"_"$FT"_"$TIMESTAMP
    SNAP=$FT"_"$TIMESTAMP
    SNAPA+=($SNAP)
    echo "-----------"
    echo "Snapshoting "$FT" as "$NS"_"$FT"_"$TIMESTAMP
    $BIN/cybergis-script-pull-wfs.sh $WFS $NS $FT $PRJ $HOST $DB $DB_USER $DB_PASS $SNAP $TEMP
    python $BIN/cybergis-script-geoserver-publish-layers.py -gs $GS -ws $WS -ds $DS -ft $SNAP --username $GS_USER --password $GS_PASS
done
LAYERS=$(printf ",%s" "${SNAPA[@]}")
LAYERS=$(echo $LAYERS | cut -c 2- )
STYLES=$(printf ",%s" "${STYLESA[@]}")
STYLES=$(echo $STYLES | cut -c 2- )
python $BIN/cybergis-script-geoserver-publish-layergroup.py -gs $GS -ws $WS -lg $LG --layers "$LAYERS" --styles "$STYLES" --username $GS_USER --password $GS_PASS
#===================#
#Kenema
FTA=( "kenema_basic_osm_buildings" "kenema_basic_osm_roads")
SNAPA=()
STYLESA= ( "cybergis_structure_buildings" "cybergis_roads_roads_minor")
for FT in "${FTA[@]}"
do
    #SNAP=$NS"_"$FT"_"$TIMESTAMP
    SNAP=$FT"_"$TIMESTAMP
    SNAPA+=($SNAP)
    echo "-----------"
    echo "Snapshoting "$FT" as "$NS"_"$FT"_"$TIMESTAMP
    $BIN/cybergis-script-pull-wfs.sh $WFS $NS $FT $PRJ $HOST $DB $DB_USER $DB_PASS $SNAP $TEMP
    python $BIN/cybergis-script-geoserver-publish-layers.py -gs $GS -ws $WS -ds $DS -ft $SNAP --username $GS_USER --password $GS_PASS
done
LAYERS=$(printf ",%s" "${SNAPA[@]}")
LAYERS=$(echo $LAYERS | cut -c 2- )
STYLES=$(printf ",%s" "${STYLESA[@]}")
STYLES=$(echo $STYLES | cut -c 2- )
python $BIN/cybergis-script-geoserver-publish-layergroup.py -gs $GS -ws $WS -lg $LG --layers "$LAYERS" --username $GS_USER --password $GS_PASS
#===================#
