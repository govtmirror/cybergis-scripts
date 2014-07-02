#!/bin/bash
#This script is a work in development and is not stable.
#This script requires curl and git to be installed
#Run this script using root's login shell under: sudo su -

DATE=$(date)

INIT_ENV=$1
INIT_CMD=$2

#==================================#

install(){
  if [[ $# -ne 9 ]]; then
    echo "Usage: cybergis-script-postgis.sh prod install [rds|local] <host> <port> <user> <password> <database> <template>"
  else
    #
    INIT_ENV=$1
    INIT_CMD=$2
    TYPE=$3
    HOST=$4
    PORT=$5
    USER=$6
    PASS=${7}
    DATABASE=$8 #likely template_postgis
    TEMPLATE=$9 #likely tempalte0
    #
    #ST_0="SELECT 'test';"
    #CMD_0="PGPASSWORD='$PASS' psql --host=$HOST --port=$PORT --username $USER -c \"$ST_0\""
    #bash --login -c $CMD_0
    ST_1="CREATE DATABASE "$DATABASE" ENCODING 'UTF8' TEMPLATE "$TEMPLATE";"
    CMD_1="PGPASSWORD='$PASS' psql --host=$HOST --port=$PORT --username $USER -c \"$ST_1\""
    bash --login -c "$CMD_1"
    CMD_2="PGPASSWORD='$PASS' psql --host=$HOST --port=$PORT --username $USER -d $DATABASE -f lib/postgis/postgis_install.sql"
    bash --login -c "$CMD_2"
    if [[ "$TYPE" = "rds" ]]; then
      CMD_3="PGPASSWORD='$PASS' psql --host=$HOST --port=$PORT --username $USER -d $DATABASE -f lib/postgis/postgis_install_rds.sql"
      bash --login -c "$CMD_3"
    fi
  fi
}

if [[ "$INIT_ENV" = "prod" ]]; then
    
    if [[ "$INIT_CMD" == "install" ]]; then
        
        if [[ $# -ne 9 ]]; then
            echo "Usage: cybergis-script-postgis.sh $INIT_ENV $INIT_CMD [rds|local] <host> <port> <user> <password> <database> <template>"
        else
            export -f install
            bash --login -c "install $INIT_ENV $INIT_CMD \"$3\" \"$4\" \"$5\" \"$6\" '${7}' \"$8\" \"$9\""
        fi
    else
        echo "Usage: cybergis-script-postgis.sh prod [install]"
    fi

else
    echo "Usage: cybergis-script-postgis.sh [prod|dev] [install]"
fi
