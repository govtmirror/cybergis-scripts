#!/bin/bash
#==========##========#
BIN=/opt/cybergis-scripts.git/bin
TIMESTAMP=$(date +%s)
#==#
GS_USER=admin
GS_PASS=geoserver
#==#
GS='http://localhost:8080/geoserver/'
#==#
PRJ='EPSG:4326'
#===================#
#Customize Layers, bbox, width, and height for each Animation
LAYERSA=( "A" "B" "C" )
LAYERS=$(printf ",%s" "${LAYERSA[@]}")
LAYERS=$(echo $LAYERS | cut -c 2- )
BBOX=<BBOX>
WIDTH=<WIDTH>
HEIGHT=<HEIGHT>
#==#
#===================#
python $BIN/cybergis-script-geoserver-animate.py -gs $GS --layers "$LAYERS" --bbox "$BBOX" --width "$WIDTH" --height "$HEIGHT" --username $GS_USER --password $GS_PASS --url
