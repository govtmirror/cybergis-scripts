#!/bin/bash

if [[ $# -ne 10 ]]; then
	echo "Usage: cybergis-script-pull-wfs.sh <wfs> <namespace> <featuretype> <projection> <dbhost> <dbname> <dbuser> <dbpass> <table> <temp>"
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
TEMP=${10}
#==#
URL="$WFS?typename=$NAMESPACE%3A$FEATURETYPE&outputFormat=$FORMAT&version=1.0.0&request=GetFeature&service=WFS"
#==#
CACHE=$NAMESPACE"_"$FEATURETYPE"_"$TIMESTAMP".geojson"
#==#
echo ""
echo "Starting pull at "$DATE
if [ -d $TEMP ] ; then
	echo "Removing data from previous pull"
	rm -fr $TEMP/$CACHE
else
	mkdir $TEMP
fi

cd $TEMP
echo "Retrieving data from "$URL
wget $URL -O $NAMESPACE"_"$FEATURETYPE".geojson"
ogr2ogr -overwrite -a_srs $PROJECTION -f "PostgreSQL" PG:"host=$DBHOST user=$DBUSER dbname=$DBNAME password=$DBPASS" $CACHE -nln "$TABLE"
echo "Finished pull of "$NAMESPACE":"$FEATURETYPE
