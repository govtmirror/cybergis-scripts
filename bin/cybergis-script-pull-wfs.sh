#!/bin/bash

if [[ $# -ne 9 ]]; then
	echo "Usage: cybergis-script-pull-wfs.sh <wfs> <namespace> <featuretype> <projection> <dbhost> <dbname> <dbuser> <dbpass> <table>"
	exit
fi
DATE=$(date)
TIMESTAMP=$(date +%s)
FORMAT=json
WFS=$1
NAMESPACE=$2
FEATURETYPE=$3
PROJECTION=$4
DBHOST=$5
DBNAME=$6
DBUSER=$7
DBPASS=$8
TABLE=$9
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
		rm -fr $TEMP/*
	fi

	mkdir $TEMP
	cd $TEMP

	echo "Retrieving data from "$URL
	wget $URL -O $NAMESPACE"_"$FEATURETYPE".geojson"
	ogr2ogr -overwrite -a_srs $PROJECTION -f "PostgreSQL" PG:"host=$DBHOST user=$DBUSER dbname=$DBNAME password=$DBPASS" $NAMESPACE"_"$FEATURETYPE".geojson" -nln "$TABLE"
	echo "Finished pull of "$NAMESPACE":"$FEATURETYPE
fi
