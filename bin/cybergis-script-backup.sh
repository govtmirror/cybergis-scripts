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
    CWD=${PWD}
    mkdir -p $OUTPUT
    IFS=$'\n' 
    for LINE in `cat $MANIFEST`; do
        if [[ ${LINE:0:1} == "#" ]]; then
            continue
        fi
        if [[ $LINE == "" ]]; then
            continue
        fi
        cd $CWD
        echo "-------------------------------"
        NAME=$(echo $LINE | cut -f1)
        SOURCE=$(echo $LINE | cut -f2)
        echo "Cloning $SOURCE to $OUTPUT/$NAME"
        if [ ! -d $OUTPUT/$NAME ]; then
            git clone $SOURCE $OUTPUT/$NAME
        fi
        cd $OUTPUT/$NAME
        git checkout master
        for branch in `git branch -a | grep remotes | grep -v HEAD | grep -v master`; do
            BRANCH_TRIMMED="$(echo -e "${branch}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
            BRANCH_NAME=${BRANCH_TRIMMED##*/}
            if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
                echo "Branch $BRANCH_NAME already exists"
            else
                git branch --track $BRANCH_NAME $BRANCH_TRIMMED
            fi
        done
        git fetch --all 
        git pull --all
    done
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
