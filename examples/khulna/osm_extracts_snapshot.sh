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
#Khulna, Bangladesh
LG=khulna_$TIMESTAMP
FTA=( "khulna_medicalcenters_osm_medical_centers" "khulna_basic_osm_buildings" "khulna_basic_osm_roads" "khulna_schools_osm_schools_areas" "khulna_landuse_osm_landuse_farmland" "khulna_landuse_osm_landuse_residential" "khulna_landuse_osm_landuse_military" "khulna_landuse_osm_landuse_forest")
SNAPA=()
STYLESA= ( "cybergis_health_medical_center" "cybergis_structure_buildings" "cybergis_basic_line_blue" "cybergis_education_schools_areas" "cybergis_landuse_farmland" "cybergis_landuse_residential" "cybergis_landuse_military" "cybergis_landuse_forest" )
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
