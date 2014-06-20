#!/bin/bash
#This script is a work in development and is not stable.
#This script requires curl and git to be installed
#Run this script using root's login shell under: sudo su -

DATE=$(date)

INIT_ENV=$1
INIT_CMD=$2

#==================================#

resize_volume(){
  echo "resize_volume"
  if [[ $# -ne 3 ]]; then
    echo "Usage: cybergis-script-ec2.sh $INIT_ENV $INIT_CMD <dev>"
  else
    INIT_ENV=$1
    INIT_CMD=$2
    DEVICE=$3
    #
    e2fsck -f $DEVICE
    resize2fs $DEVICE
  fi
}

if [[ "$INIT_ENV" = "prod" ]]; then
    
    if [[ "$INIT_CMD" == "resize" ]]; then
        
        if [[ $# -ne 3 ]]; then
            echo "Usage: cybergis-script-ec2.sh $INIT_ENV $INIT_CMD"
        else
            export -f resize_volume
            bash --login -c resize_volume
        fi
    else
        echo "Usage: cybergis-script-ec2.sh prod [resize]"
    fi

else
    echo "Usage: cybergis-script-ec2.sh [prod|dev] [resize]"
fi
