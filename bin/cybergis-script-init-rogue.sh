#!/bin/bash
#This script is a work in development and is not stable.
#This script requires curl and git to be installed
#Run this script using rogue's login shell under: sudo su - <user>

DATE=$(date)
RUBY_VERSION="2.0.0-p353"
CTX_GEOGIT="/geoserver/geogit/"
FILE_SETTINGS="/var/lib/geonode/rogue_geonode/rogue_geonode/settings.py"

INIT_ENV=$1
INIT_CMD=$2

#==================================#
#     Thes following functions are for installation #

init_user(){
  adduser rogue --disabled-password --home /home/rogue --shell /bin/bash
}

install_rvm(){
  curl -L https://get.rvm.io | bash -s stable
}

install_gems(){
  #
  rvm get stable
  rvm list known
  rvm install "ruby-$RUBY_VERSION"
  rvm --default use $RUBY_VERSION
  ruby -v
  #
  gem install chef --version 11.8.0 --no-rdoc --no-ri --conservative
  gem install solve --version 0.8.2
  gem install nokogiri --version 1.6.1
  gem install berkshelf --version 2.0.14 --no-rdoc --no-ri
  gem list
  #
}

install_geonode(){
  echo "install_geonode"
  if [[ $# -ne 3 ]]; then
    echo "Usage: cybergis-script-init-rogue.sh $INIT_ENV $INIT_CMD <fqdn>"
  else
    INIT_ENV=$1
    INIT_CMD=$2
    FQDN=$3
    #
    cd /opt
    git clone https://github.com/ROGUE-JCTD/rogue-chef-repo.git
    mkdir chef-run
    cp -r /opt/rogue-chef-repo/solo/* chef-run/
    cd chef-run
    sed -i "s/dev.rogue.lmnsolutions.com/$FQDN/g" dna.json
    chmod 755 run.sh
    #
    bash --login run.sh
  fi
}

install_awscli(){
    #
    if ! type "pip" &> /dev/null; then
        apt-get install python-pip
    fi
    pip install awscli
    #
}


#==================================#
#     Thes following functions are for configuration #

add_server(){
  if [[ $# -ne 6 ]]; then
      echo "Usage: cybergis-script-init-rogue.sh $INIT_ENV $INIT_CMD [tms] <name> <url>"
  else
      INIT_ENV=$1
      INIT_CMD=$2
      TYPE=$3
      NAME=$4
      URL=$5
      FILE_SETTINGS=$6
      if [[ "$TYPE" == "tms" ]]; then
          JSON='{\"source\":{\"ptype\":\"gxp_tmssource\",\"name\":\"'$NAME'\",\"url\":\"'$URL'\"},\"visibility\":True}'
          LINE="MAP_BASELAYERS.append($JSON)"
          CMD1='echo "" >> "'$FILE_SETTINGS'"'
          CMD2='echo "'$LINE'" >> "'$FILE_SETTINGS'"'
          bash --login -c "$CMD1"
          bash --login -c "$CMD2"
      elif [[ "$TYPE" == "wms" ]]; then
          JSON='{\"source\":{\"ptype\":\"gxp_wmscsource\",\"restUrl\":\"/gs/rest\",\"name\":\"'$NAME'\",\"url\":\"'$URL'\"},\"visibility\":True}'
          LINE="MAP_BASELAYERS.append($JSON)"
          CMD1='echo "" >> "'$FILE_SETTINGS'"'
          CMD2='echo "'$LINE'" >> "'$FILE_SETTINGS'"'
          bash --login -c "$CMD1"
          bash --login -c "$CMD2"
      elif [[ "$TYPE" == "geonode" ]]; then
          JSON='{\"source\":{\"ptype\":\"gxp_wmscsource\",\"restUrl\":\"/gs/rest\",\"name\":\"'$NAME'\",\"url\":\"'$URL'/geoserver/wms\"},\"visibility\":True}'
          LINE="MAP_BASELAYERS.append($JSON)"
          CMD1='echo "" >> "'$FILE_SETTINGS'"'
          CMD2='echo "'$LINE'" >> "'$FILE_SETTINGS'"'
          bash --login -c "$CMD1"
          bash --login -c "$CMD2"
      else
          echo "Usage: cybergis-script-init-rogue.sh $INIT_ENV $INIT_CMD [tms|geonode] <name> <url>"
      fi
  fi
}

add_remote(){
  echo $URL  
  if [[ $# -ne 10 ]]; then
      echo "Usage: cybergis-script-init-rogue.sh $INIT_ENV $INIT_CMD <user:password> <localRepoName> <localGeonodeURL> <remoteName> <remoteRepoName> <remoteGeoNodeURL> <remoteUser> <remotePassword>"
  else
      INIT_ENV=$1
      INIT_CMD=$2
      USERPASS=$3
      LOCAL_REPO_NAME=$4
      LOCAL_GEONODE_URL=$5
      REMOTE_NAME=$6
      REMOTE_REPO_NAME=$7
      REMOTE_GEONODE_URL=$8
      REMOTE_USER=$9
      REMOTE_PASS=${10}
      
      REPO_URL="$LOCAL_GEONODE_URL/geoserver/geogit/$LOCAL_REPO_NAME/"
      REMOTE_URL="$REMOTE_GEONODE_URL/geoserver/geogit/$REMOTE_REPO_NAME/"
      CMD="add_remote_2 $INIT_ENV $INIT_CMD \"$USERPASS\" \"$REPO_URL\" \"$REMOTE_NAME\" \"$REMOTE_URL\" \"$REMOTE_USER\" \"$REMOTE_PASS\""
      bash --login -c "$CMD"
  fi
}

add_remote_2(){
  if [[ $# -ne 8 ]]; then
      echo "Usage: cybergis-script-init-rogue.sh $INIT_ENV $INIT_CMD <user:password> <repoURL> <remoteName> <remoteURL> <remoteUser> <remotePassword>"
  else
      INIT_ENV=$1
      INIT_CMD=$2
      USERPASS=$3
      REPO_URL=$4
      REMOTE_NAME=$5
      REMOTE_URL=$6
      REMOTE_USER=$7
      REMOTE_PASS=$8
      
      CTX="remote"
      QS="user=$REMOTE_USER&password=$REMOTE_PASS&output_format=JSON&remoteName=$REMOTE_NAME&remoteURL=$REMOTE_URL"
      URL="$REPO_URL$CTX?$QS"
      
      CMD='curl -u '$USERPASS' "'$URL'"'
      #echo $CMD
      bash --login -c "$CMD"
  fi
}


if [[ "$INIT_ENV" = "prod" ]]; then
    
    if [[ "$INIT_CMD" == "user" ]]; then
        
        if [[ $# -ne 2 ]]; then
	    echo "Usage: cybergis-script-init-rogue.sh $INIT_ENV $INIT_CMD"
        else
            export -f init_user
            bash --login -c init_user
        fi
    
    elif [[ "$INIT_CMD" == "rvm" ]]; then
        
        if [[ $# -ne 2 ]]; then
	    echo "Usage: cybergis-script-init-rogue.sh $INIT_ENV $INIT_CMD"
        else
            export -f install_rvm
            bash --login -c install_rvm
        fi
    
    elif [[ "$INIT_CMD" == "gems" ]]; then
        
        if [[ $# -ne 2 ]]; then
	    echo "Usage: cybergis-script-init-rogue.sh $INIT_ENV $INIT_CMD"
        else
            export -f install_gems
            bash --login -c install_gems
        fi
    
    elif [[ "$INIT_CMD" == "geonode" ]]; then
        
        if [[ $# -ne 3 ]]; then
	    echo "Usage: cybergis-script-init-rogue.sh $INIT_ENV $INIT_CMD <fqdn>"
        else
            export -f install_geonode
            bash --login -c "install_geonode $INIT_ENV $INIT_CMD \"$3\""
        fi

    elif [[ "$INIT_CMD" == "server" ]]; then
        
        if [[ $# -ne 5 ]]; then
	    echo "Usage: cybergis-script-init-rogue.sh $INIT_ENV $INIT_CMD [geonode|wms|tms] <name> <url>"
        else
            export -f add_server
            bash --login -c "add_server $INIT_ENV $INIT_CMD $3 \"$4\" \"$5\" \"$FILE_SETTINGS\""
        fi
    elif [[ "$INIT_CMD" == "remote" ]]; then
        
        if [[ $# -ne 10 ]]; then
	    echo "Usage: cybergis-script-init-rogue.sh $INIT_ENV $INIT_CMD <user:password> <localRepoName> <localGeonodeURL> <remoteName> <remoteRepoName> <remoteGeoNodeURL> <remoteUser> <remotePassword>"
        else
            export -f add_remote
            export -f add_remote_2
            bash --login -c "add_remote $INIT_ENV $INIT_CMD \"$3\" \"$4\" \"$5\" \"$6\" \"$7\" \"$8\" \"$9\" \"${10}\""
        fi
    elif [[ "$INIT_CMD" == "remote2" ]]; then
        
        if [[ $# -ne 8 ]]; then
	    echo "Usage: cybergis-script-init-rogue.sh $INIT_ENV $INIT_CMD <user:password> <repoURL> <remoteName> <remoteURL> <remoteUser> <remotePassword>"
        else
            export -f add_remote_2
            bash --login -c "add_remote_2 $INIT_ENV $INIT_CMD \"$3\" \"$4\" \"$5\" \"$6\" \"$7\" \"$8\""
        fi
    else
        echo "Usage: cybergis-script-init-rogue.sh prod [use|rvm|gems|geonode|server]"
    fi

else
    echo "Usage: cybergis-script-init-rogue.sh [prod|dev] [use|rvm|gems|geonode|server|remote|remote2]"
fi

