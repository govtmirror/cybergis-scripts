#!/bin/bash

if [[ $# -ne 6 ]]; then
	echo "Usage: cybergis-script-pull-shapefile.sh <url> <shapefile> <dbname> <dbuser> <dbpass> <table>"
	exit
fi
DATE=$(date)
FORMAT=json
URL=$1
SHAPEFILE=$2
DBNAME=$3
DBUSER=$4
DBPASS=$5
TABLE=$6
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
	wget $URL -O pull.zip
	unzip pull.zip
	ogr2ogr -overwrite -a_srs EPSG:900913 -f "PostgreSQL" PG:"host=localhost user=$DBUSER dbname=$DBNAME password=$DBPASS" $SHAPEFILE -nln "$TABLE"
	echo "Pull completed"
fi
