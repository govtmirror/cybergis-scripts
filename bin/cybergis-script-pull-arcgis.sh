#!/bin/bash

if [[ $# -ne 6 ]]; then
	echo "Usage: cybergis-script-pull-arcgis.sh <service> <field> <dbname> <dbuser> <dbpass> <table>"
	exit
fi
DATE=$(date)
FORMAT=json
SERVICE=$1
FIELD=$2
DBNAME=$3
DBUSER=$4
DBPASS=$5
TABLE=$6
URL="$SERVICE?where=$FIELD+%3D+$FIELD&outfields=*&f=$FORMAT"
TEMP=/tmp/cybergis-pull

if [[ $EUID -ne 0 ]]; then
  echo "You must be a root user" 2>&1
  exit 1
else
	echo ""
	echo "Starting pull at "$DATE
	if [ -d $TEMP ] ; then
		echo "Removing data from previous pull"
		rm -fr $TEMP
	fi

	mkdir $TEMP
	
	cd $TEMP

	echo "Retrieving data from "$URL
	wget $URL -O pull_arcgis.json
        ogr2ogr -overwrite -s_srs EPSG:900913 -a_srs EPSG:900913 -f GeoJSON pull.geojson pull_arcgis.json OGRGeoJSON
	ogr2ogr -overwrite -a_srs EPSG:900913 -f "PostgreSQL" PG:"host=localhost user=$DBUSER dbname=$DBNAME password=$DBPASS" pull.geojson -nln "$TABLE"
	echo "Pull completed"
fi
