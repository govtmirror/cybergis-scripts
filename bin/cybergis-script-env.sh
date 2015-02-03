#!/bin/bash
#This script is a work in development and is stable,
#but may change to stay up to date with other projects.
#This script requires curl and git to be installed
#Run this script using root's login shell under: sudo su -

DATE=$(date)

ENV=$1
CMD=$2
#==================================#
geonode(){
  echo "geonode"
  if [ $# -ne 2 ] && [ $# -ne 3 ]; then
    echo "Usage: cybergis-script-env.sh geonode [install|reset]"
  else
    ENV=$1
    CMD=$2
    #
    if [[ "$CMD" = "install" ]]; then
      #
      if [[ $# -ne 2 ]]; then
        echo "Usage: cybergis-script-env.sh geonode install"
      else
        bash --login -c "geonode_install"
      fi
      #
    elif [[ "$CMD" = "reset" ]]; then
      #
      source ~/.bash_aliases
      workon geonode
      source ~/.venvs/geonode/bin/activate
      #
      cd ~/geonode
      paver stop
      #paver reset
      paver reset_hard
      if [[ $# -ne 3 ]]; then
        paver setup
      else
        paver setup --geoserver "${3}"
      fi
      paver start -b 0.0.0.0:8000
      #
    else
      echo "Usage: cybergis-script-env.sh geonode [install|reset]"
    fi
  fi
}

rogue(){
  echo "rogue"
  if [[ $# -ne 2 ]]; then
    echo "Usage: cybergis-script-env.sh rogue [install|reset]"
  else
    ENV=$1
    CMD=$2
    #
    if [[ "$CMD" = "install" ]]; then
      #
      bash --login -c "geonode_install"
      #===============#
      #Install ROGUE Components
      source ~/.bash_aliases
      mkvirtualenv rogue_geonode
      workon rogue_geonode
      #
    elif [[ "$CMD" = "reset" ]]; then
      #
      source ~/.bash_aliases
      workon rogue_geonode
      #
      cd ~/rogue_geonode
      paver stop
      paver reset
      #paver reset_hard
      paver build_geoserver
      if [[ $# -ne 3 ]]; then
        paver setup
      else
        paver setup --geoserver ${3}
      fi
      paver start -b 0.0.0.0:8000
      #
    else
      echo "Usage: cybergis-script-env.sh geonode [install|reset]"
    fi
  fi
}

geonode_install(){
  echo "geonode_install"
  sudo apt-get update
  # Add UbuntuGIS Repository to get latest GDAL package
  sudo apt-get install -y python-software-properties
  sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
  # Add respository for static development
  sudo add-apt-repository -y ppa:chris-lea/node.js
  #
  sudo apt-get update
  # Essential build tools and libraries
  sudo apt-get install -y build-essential libxml2-dev libxslt1-dev libjpeg-dev gettext git python-dev python-pip python-virtualenv
  sudo apt-get install -y libgdal1h libgdal-dev python-gdal
  sudo apt-get install -y libgeos-dev libpq-dev
  # Python and Django dependencies with official packages
  sudo apt-get install -y python-lxml python-psycopg2 python-django python-bs4 python-multipartposthandler transifex-client python-nose python-django-nose python-django-pagination python-django-extensions python-httplib2
  # Java dependencies
  sudo apt-get install -y --force-yes openjdk-6-jdk ant maven2 --no-install-recommends
  #
  sudo apt-get install -y nodejs
  sudo npm install -y -g bower
  sudo npm install -y -g grunt-cli
  #
  #Install python packages for development
  sudo pip install virtualenvwrapper paver

  #Add all these lines to ~/.bash_aliases
  echo 'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python' >> ~/.bash_aliases
  echo 'export WORKON_HOME=~/.venvs' >> ~/.bash_aliases
  echo 'source /usr/local/bin/virtualenvwrapper.sh'>> ~/.bash_aliases
  echo 'export PIP_DOWNLOAD_CACHE=$HOME/.pip-downloads' >> ~/.bash_aliases
  #echo 'workon geonode' >> ~/.bash_aliases
  #===============#
  #Create GeoNode Virtual Environment
  source ~/.bash_aliases
  mkvirtualenv geonode
  workon geonode
  #===============#
  #Install Django Dependencies
  pip install pillow
  pip install pinax-theme-bootstrap==3.0a11 pinax-theme-bootstrap-account==1.0b2
  pip install django-tastypie django-autocomplete-light django-mptt
  pip install django-taggit django-taggit-templatetags django-modeltranslation
  pip install django-jsonfield django-downloadview django-pagination django-friendly-tag-loader django-extensions
  pip install django-geoexplorer django-leaflet 
  #
  #===============#
  #Install GDAL
  pip install --no-install GDAL==1.10.0
  cd /home/vagrant/.venvs/geonode/build/GDAL
  sed -i "s/\.\.\/\.\.\/apps\/gdal-config/\/usr\/bin\/gdal-config/g" setup.cfg
  python setup.py build_ext --include-dirs=/usr/include/gdal
  pip install --no-download GDAL==1.10.0
  #===============#
  #Install GeoNode
  cd ~
  pip install -e geonode
  #
  #cd ~/geonode
}

maploom(){
  echo "maploom"
  if [[ $# -ne 2 ]]; then
    echo "Usage: cybergis-script-env.sh maploom [install|reset]"
  else
    ENV=$1
    CMD=$2
    
    if [[ "$CMD" = "install" ]]; then
      sudo apt-get update
      #
      sudo apt-get install -y python-software-properties
      #sudo add-apt-repository ppa:chris-lea/node.js
      sudo apt-add-repository ppa:chris-lea/node.js-legacy
      #
      sudo apt-get update
      #
      sudo apt-get install -y curl vim git
      #For compiling nodejs, version 8.22
      sudo apt-get install -y make gcc
      #
      #sudo apt-get install -y nodejs nodejs-dev npm
      #Need old version of NodeJS for dev and npm.
      #See: http://stackoverflow.com/questions/16898001/installing-a-specific-node-version-in-ubuntu
      #See: https://launchpad.net/~chris-lea/+archive/ubuntu/node.js-legacy
      #See: https://groups.google.com/forum/#!topic/nodejs/9HjStFy2ohY
      sudo apt-get install nodejs=0.8.28-1chl1~precise1
      sudo apt-get install -y nodejs-dev npm
      sudo apt-get install -y npm
      sudo npm config set registry http://registry.npmjs.org/
      #
      #sudo npm -g install grunt-cli karma bower
      sudo npm -g install grunt-cli bower
      #
      cd ~/MapLoom
      npm install grunt-karma@0.9.x wordwrap
      sudo npm install
      bower install
      grunt watch
      #
    elif [[ "$CMD" = "reset" ]]; then
      # 
      echo "reset"
      #
    else
      echo "Usage: cybergis-script-env.sh maploom [install|reset]"
    fi
  fi
}

geogig(){
  echo "geogig"
  if [[ $# -ne 2 ]]; then
    echo "Usage: cybergis-script-env.sh geogig [install|reset]"
    echo "Requires: unzip"
  else
    ENV=$1
    CMD=$2

    if [[ "$CMD" = "install" ]]; then
      sudo apt-get update
      #
      sudo apt-get install -y openjdk-7-jdk
      #Download Builds
      mkdir ~/ws
      mkdir ~/ws/build
      cd ~/ws/build
      wget http://sourceforge.net/projects/geoserver/files/GeoServer/2.6-RC1/geoserver-2.6-RC1-bin.zip 
      wget https://s3.amazonaws.com/hiu-build/geogig-cli-app-1.0-SNAPSHOT.zip
      wget https://s3.amazonaws.com/hiu-build/gs-geogig-2.6-SNAPSHOT-shaded-plugin.jar
      #
      cd /opt
      sudo git clone https://github.com/state-hiu/cybergis-osm-mappings.git cybergis-osm-mappings.git
      sudo git clone https://github.com/state-hiu/cybergis-styles.git cybergis-styles.git
      sudo git clone https://github.com/state-hiu/cybergis-client-examples.git cybergis-client-examples.git
      sudo git clone https://github.com/state-hiu/cybergis-osm-extractions.git cybergis-osm-extractions.git
      #Install GeoGig Cli
      sudo mkdir /opt/geogig
      sudo unzip ~/ws/build/geogig-cli-app-1.0-SNAPSHOT.zip -d /opt/geogig
      sudo cp /opt/cybergis-scripts.git/profile/geogig.sh /etc/profile.d/
      #Install GeoServer
      mkdir ~/ws/gs
      unzip ~/ws/build/geoserver-2.6-RC1-bin.zip -d ~/ws/gs
      cp ~/ws/build/gs-geogig-2.6-SNAPSHOT-shaded-plugin.jar ~/ws/gs/geoserver-2.6-RC1/webapps/geoserver/WEB-INF/lib/
      #Make folder to store GeoGig Repositories
      mkdir ~/ws/geogig
      mkdir ~/ws/geogig/repo
    elif [[ "$CMD" = "clear" ]]; then
      # 
      echo "clear"
      rm -fr ~/ws
      rm -fr ~/etc/profile.d/geogig.sh
      sudo rm -fr /opt/geogig
      #
    else
      echo "Usage: cybergis-script-env.sh geogig [install|clear]"
    fi
  fi

}

ittc(){
  echo "ittc"
  if [[ $# -ne 2 ]]; then
    echo "Usage: cybergis-script-env.sh ittc [install|reset]"
  else
    ENV=$1
    CMD=$2
    #
    if [[ "$CMD" = "install" ]]; then
      sudo apt-get update
      #
      #sudo apt-get install postgresql-client-common postgresql-client-9.1
      sudo apt-get install -y libgeos-dev libproj-dev
      sudo apt-get install -y gdal-bin python-gdal python-numpy
      #
    elif [[ "$CMD" = "reset" ]]; then
      # 
      echo "reset"
      #
    else
      echo "Usage: cybergis-script-env.sh ittc [install|reset]"
    fi
  fi
}

if [[ "$ENV" = "geonode" ]]; then
    
    if [ $# -ne 2 ] && [ $# -ne 3 ]; then
        echo "Usage: cybergis-script-env.sh geonode [install|reset]"
        echo "or"
        echo "Usage: cybergis-script-env.sh geonode reset geoserver_url"
        echo "GeoServer URL can be remote or local file (file:///.../...)"
    else
        export -f geonode_install
        export -f geonode
        if [[ "$CMD" = "install" ]]; then
            bash --login -c "geonode $ENV $CMD"
        elif [[ "$ENV" = "reset" ]]; then
            if [[ $# -eq 2 ]]; then
                bash --login -c "geonode $ENV $CMD"
            else
                bash --login -c "geonode $ENV $CMD '${3}'"
            fi
        fi
    fi
    
elif [[ "$ENV" = "rogue" ]]; then
    
    if [[ $# -ne 2 ]]; then
        echo "Usage: cybergis-script-env.sh rogue [install|reset]"
    else
        export -f geonode_install
        export -f rogue
        bash --login -c "rogue $ENV $CMD"
    fi

elif [[ "$ENV" = "maploom" ]]; then
    
    if [[ $# -ne 2 ]]; then
        echo "Usage: cybergis-script-env.sh maploom [install|reset]"
    else
        export -f maploom
        bash --login -c "maploom $ENV $CMD"
    fi

elif [[ "$ENV" = "ittc" ]]; then
    
    if [[ $# -ne 2 ]]; then
        echo "Usage: cybergis-script-env.sh ittc [install|reset]"
    else
        export -f ittc
        bash --login -c "ittc $ENV $CMD"
    fi

elif [[ "$ENV" = "geogig" ]]; then

    if [[ $# -ne 2 ]]; then
        echo "Usage: cybergis-script-env.sh geogig [install|reset]"
    else
        export -f geogig
        bash --login -c "geogig $ENV $CMD"
    fi

else
    echo "Usage: cybergis-script-env.sh [geonode|rogue|maploom|geogig|ittc]"
fi
