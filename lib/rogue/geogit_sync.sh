#!/bin/bash
DATE=$(date)
CTX_GEOGIT="/geoserver/geogit/"
GEONODE_LOCAL="http://localhost"
PYTHON=/var/lib/geonode/bin/python
#MANAGE=/var/lib/geonode/rogue_geonode/manage.py
DIR=/var/lib/geonode/rogue_geonode
#==#
if [[ $# -ne 5 ]]; then
    echo "Usage: geogit_sync.sh <direction> <user> <password> <repo> <remote>"
else
    DIRECTION=$1
    USER=$2
    PASSWORD=$3
    REPO=$4
    REMOTE=$5
    #echo "Running: "$PYTHON manage.py geogit-sync --username $USER --password $PASSWORD --url "$GEONODE_LOCAL$CTX_GEOGIT$REPO/" --remote $REMOTE
    #==#
    cd $DIR
    $PYTHON manage.py geogit-sync --direction $DIRECTION --username $USER --password $PASSWORD --url "$GEONODE_LOCAL$CTX_GEOGIT$REPO/" --remote $REMOTE
fi
