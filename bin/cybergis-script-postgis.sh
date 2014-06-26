#!/bin/bash
#This script is a work in development and is not stable.
#This script requires curl and git to be installed
#Run this script using root's login shell under: sudo su -

DATE=$(date)

INIT_ENV=$1
INIT_CMD=$2

#==================================#

install(){
  echo "install"
  if [[ $# -ne 4 ]]; then
    echo "Usage: cybergis-script-postgis prod install <host> <port> <user> <password>"
  else
    #
    INIT_ENV=$1
    INIT_CMD=$2
    HOST=$3
    PORT=$4
    USER=$5
    PASS=$6
    #
    PGPASSWORD=$PASS psql --host=$HOST --port=$PORT --username $USER --password -f lib/postgis/postgis_install.sql
  fi
}

if [[ "$INIT_ENV" = "prod" ]]; then
    
    if [[ "$INIT_CMD" == "install" ]]; then
        
        if [[ $# -ne 4 ]]; then
            echo "Usage: cybergis-script-postgis.sh $INIT_ENV $INIT_CMD <host> <user> <password> <dbname>"
        else
            export -f tune
            bash --login -c "tune $INIT_ENV $INIT_CMD \"$3\" \"$4\""
        fi
    else
        echo "Usage: cybergis-script-postgis.sh prod [install]"
    fi

else
    echo "Usage: cybergis-script-postgis.sh [prod|dev] [install]"
fi
