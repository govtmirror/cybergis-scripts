#!/bin/bash
#=================#
#Based on scripts from https://github.com/ROGUE-JCTD/rogue-scripts
#=================#
DATE=$(date)
CTX_GEOGIT="/geoserver/geogit/"
GEONODE_LOCAL="http://localhost"
PYTHON=/var/lib/geonode/bin/python
#MANAGE=/var/lib/geonode/rogue_geonode/manage.py
DIR=/var/lib/geonode/rogue_geonode
#==#
# Auto-Sync Delay (in seconds)
AUTO_SYNC_DELAY=60
# Sync Attempts
SYNC_ATTEMPTS=10
# This will track whether or not an error occurred
ERROR_OCCURED=0
#=================#
if [[ $# -ne 7 ]]; then
    echo "Usage: geogit_sync_osm.sh <repo> <remote> <log_file> <error_file>"
    echo 'authorname and authoremail used when merging non-conflicting branches'
    echo 'repo points to the staging repo'
    echo 'remote points to the live repo to be updated'
else
    DIRECTION=$1
    USER=$2
    PASSWORD=$3
    REPO=$4
    REMOTE=$5
    AUTHORNAME=$6
    AUTHOREMAIL=$7
    LOG_FILE=$8
    ERROR_FILE=$9
    #=================#
    cd $REPO
    #=================#
    if [ -f $ERROR_FILE ]; then
        exit 255
    fi
    #=================#
    exec 1>$LOG_FILE
    #=================#
    printf "\nUpdating OSM Data...";
    printf "\n===========================\n";
    geogit checkout master
    geogit osm download --update
    geogit checkout master
    #=================#
    printf "\n===========================";
    printf "\nSynchronizing repository...";
    printf "\n===========================\n";
    for i in `seq 1 $SYNC_ATTEMPTS`
    do
	echo "Attempt $i of $SYNC_ATTEMPTS."
        ERROR_OCCURED=0
	geogit pull $REMOTE
        EXIT_CODE=$?
        if [ $EXIT_CODE -gt 0 ]; then
         ERROR_OCCURED=255
        fi
        OUTPUT=$(geogit push $REMOTE)
        EXIT_CODE=$?
        echo $OUTPUT
        if [ $EXIT_CODE -gt 0 ]; then 
            if [  "$OUTPUT" != "Nothing to push." ]; then
                ERROR_OCCURED=255
            fi
        fi
	if [ $ERROR_OCCURED -eq 0 ]; then
         break
	fi
        sleep $AUTO_SYNC_DELAY
    done
    
    if [ $ERROR_OCCURED -eq 255 ]; then
        #cat $LOG_FILE | mail -s "$EMAIL_SUBJECT" $EMAIL_ADDRESS
        echo $ERROR_MESSAGE >> $ERROR_FILE
    fi
fi
