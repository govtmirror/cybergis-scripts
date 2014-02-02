#!/bin/bash

if [[ $# -ne 7 ]]; then
	echo "Usage: cybergis-script-pull-wfs.sh <wfs> <namespace> <featuretype> <dbname> <dbuser> <dbpass> <table>"
	exit
fi
DATE=$(date)
FORMAT=json
WFS=$1
NAMESPACE=$2
FEATURETYPE=$3
DBNAME=$4
DBUSER=$5
DBPASS=$6
TABLE=$7
URL="$WFS?typename=$NAMESPACE%3A$FEATURETYPE&outputFormat=$FORMAT&version=1.0.0&request=GetFeature&service=WFS"
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

	echo "Retreiving data from "$URL
	wget $URL -O pull.geojson
	ogr2ogr -overwrite -a_srs EPSG:900913 -f "PostgreSQL" PG:"host=localhost user=$DBUSER dbname=$DBNAME password=$DBPASS" pull.geojson -nln "$TABLE"
	echo "Pull completed"
fi
