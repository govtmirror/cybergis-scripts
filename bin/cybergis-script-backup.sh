#!/bin/bash

DATE=$(date)
BACKUP_CMD=$1
#==================================#
backup_repos(){
  echo "backup_repos"
  if [[ $# -ne 3 ]]; then
    echo "Usage: cybergis-script-backup.sh repos <manifest> <output>"
  else
    BACKUP_CMD=$1
    MANIFEST=$2
    OUTPUT=$3
    #
    mkdir -p $OUTPUT
    while read line; do
        NAME=$(cat $MANIFEST | cut -f1)
        SOURCE=$(cat $MANIFEST | cut -f2)
        git clone $SOURCE $OUTPUT/$NAME
    done <$MANIFEST
  fi
}

if [[ "$BACKUP_CMD" == "repos" ]]; then
        
    if [[ $# -ne 3 ]]; then
        echo "Usage: cybergis-script-backup.sh repos <manifest> <output>"
    else
        export -f backup_repos
        bash --login -c "backup_repos $BACKUP_CMD '${2}' '${3}'"
    fi
    
else
    echo "Usage: cybergis-script-backup.sh [repos]"
fi
