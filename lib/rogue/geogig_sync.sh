#!/bin/bash
DATE=$(date)
CTX_GEOGIG="/geoserver/geogig/"
GEONODE_LOCAL="http://localhost"
PYTHON=/var/lib/geonode/bin/python
#MANAGE=/var/lib/geonode/rogue_geonode/manage.py
DIR=/var/lib/geonode/rogue_geonode
#==#
if [[ $# -ne 7 ]]; then
    echo "Usage: geogig_sync.sh <direction> <user> <password> <repo> <remote> <authorname> <authoremail>"
    echo 'authorname and authoremail used when merging non-conflicting branches'
else
    DIRECTION=$1
    USER=$2
    PASSWORD=$3
    REPO=$4
    REMOTE=$5
    AUTHORNAME=$6
    AUTHOREMAIL=$7
    #echo "Running: "$PYTHON manage.py geogit-sync --username $USER --password $PASSWORD --url "$GEONODE_LOCAL$CTX_GEOGIG$REPO/" --remote $REMOTE
    #==#
    cd $DIR
    $PYTHON manage.py geogit-sync --direction $DIRECTION --username $USER --password $PASSWORD --url "$GEONODE_LOCAL$CTX_GEOGIG$REPO/" --remote $REMOTE --authorname $AUTHORNAME --authoremail $AUTHOREMAIL
fi
