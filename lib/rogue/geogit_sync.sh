#!/bin/bash
DATE=$(date)
CTX_GEOGIT="/geoserver/geogit/"
GEONODE_LOCAL="http://localhost"
PYTHON=/var/lib/geonode/bin/python
MANAGE=/var/lib/geonode/rogue_geonode/manage.py
#==#
if [[ $# -ne 4 ]]; then
    echo "Usage: geogit_sync.sh <user> <password> <repo> <remote>"
else
    USER=$1
    PASSWORD=$2
    REPO=$3
    REMOTE=$4
    #==#
    $PYTHON manage.py geogit-sync --username $ADMIN --password $PASSWORD --url "$GEONODE_LOCAL$CTX_GEOGIT$REPO/" --remote $REMOTE
fi
