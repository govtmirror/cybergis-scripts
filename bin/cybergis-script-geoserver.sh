#!/bin/bash
#This script is a work in development and is not stable.
#This script requires curl and git to be installed
#Run this script using root's login shell under: sudo su -

DATE=$(date)

INIT_ENV=$1
INIT_CMD=$2

#==================================#
backup(){
  echo "backup"
  if [[ $# -ne 3 ]]; then
    echo "Usage: cybergis-script-geoserver.sh $INIT_ENV $INIT_CMD <repo>"
  else
    GEOSERVER_DATA='/var/lib/opengeo/geoserver'
    #
    INIT_ENV=$1
    INIT_CMD=$2
    REPO=$3
    #
    #Initialize Git Repo Defaults
    /etc/init.d/tomcat6 stop
    mkdir -p $REPO
    cd $REPO
    git init
    cp -R $GEOSERVER_DATA/* .
    git add .
    git commit -m "update to $GEOSERVER_DATA repo"
    #
    /etc/init.d/tomcat6 start
  fi
}
tune(){
  echo "tune"
  if [[ $# -ne 4 ]]; then
    echo "Usage: cybergis-script-geoserver.sh $INIT_ENV $INIT_CMD <repo> <Xmx>"
    echo "Xmx = maximum heap size for JVM."
  else
    DEFAULTS_TOMCAT6='/etc/default/tomcat6'
    #
    INIT_ENV=$1
    INIT_CMD=$2
    REPO=$3
    XMX=$4
    #
    #Initialize Git Repo Defaults
    mkdir -p $REPO
    cd $REPO
    git init
    cp /etc/default/* .
    git add .
    git commit -m "update to /etc/defaults repo"
    #
    #Rebuild /etc/default/tomcat6
    rm $DEFAULTS_TOMCAT6
    touch $DEFAULTS_TOMCAT6
    chmod 644 $DEFAULTS_TOMCAT6
    echo '# Run Tomcat as this user ID. Not setting this or leaving it blank will use the' >> $DEFAULTS_TOMCAT6
    echo '# default of tomcat6.' >> $DEFAULTS_TOMCAT6
    echo 'TOMCAT6_USER=tomcat6' >> $DEFAULTS_TOMCAT6
    echo '' >> $DEFAULTS_TOMCAT6
    echo '# Run Tomcat as this group ID. Not setting this or leaving it blank will use' >> $DEFAULTS_TOMCAT6
    echo '# the default of tomcat6.' >> $DEFAULTS_TOMCAT6 
    echo 'TOMCAT6_GROUP=tomcat6' >> $DEFAULTS_TOMCAT6
    echo '' >> $DEFAULTS_TOMCAT6
    echo 'JAVA_OPTS="-Djava.awt.headless=true"' >> $DEFAULTS_TOMCAT6
    echo 'unset LC_ALL' >> $DEFAULTS_TOMCAT6
    echo 'OPENGEO_OPTS="-Djava.awt.headless=true -Xms512M -Xmx'$XMX' -XX:+UseParallelOldGC -XX:+UseParallelGC -XX:NewRatio=2 -XX:+AggressiveOpts -Xrs -XX:PerfDataSamplingInterval=500 -XX:MaxPermSize=256m -Dorg.geotools.referencing.forceXY=true -DGEOEXPLORER_DATA=/var/lib/opengeo/geoexplorer"'  >> $DEFAULTS_TOMCAT6
    echo 'JAVA_OPTS="$JAVA_OPTS $OPENGEO_OPTS"' >> $DEFAULTS_TOMCAT6
    #
    #Copy over any changes
    cd $REPO
    cp /etc/default/* .
    git add .
    git commit -m "update to /etc/defaults repo"
    #
    /etc/init.d/tomcat6 restart
  fi
}

if [[ "$INIT_ENV" = "prod" ]]; then
    
    if [[ "$INIT_CMD" == "backup" ]]; then
        
        if [[ $# -ne 3 ]]; then
            echo "Usage: cybergis-script-geoserver.sh $INIT_ENV $INIT_CMD <repo>"
        else
            export -f backup
            bash --login -c "backup $INIT_ENV $INIT_CMD \"$3\""
        fi
    elif [[ "$INIT_CMD" == "tune" ]]; then
        
        if [[ $# -ne 4 ]]; then
            echo "Usage: cybergis-script-geoserver.sh $INIT_ENV $INIT_CMD <repo> <Xmx>"
        else
            export -f tune
            bash --login -c "tune $INIT_ENV $INIT_CMD \"$3\" \"$4\""
        fi
    else 
    
        echo "Usage: cybergis-script-geoserver.sh prod [tune]"
    fi

else
    echo "Usage: cybergis-script-geoserver.sh [prod|dev] [backup|tune]"
fi
