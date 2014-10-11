#!/bin/bash
#This script is a work in development and is not stable.
#This script requires curl and git to be installed
#Run this script using root's login shell under: sudo su -

DATE=$(date)

ENV=$1
CMD=$2
#==================================#
#####################
###!!!!!! Still under development.  Not stable!!!!!!!!!!!!!##############
geonode(){
  echo "geonode"
  if [[ $# -ne 2 ]]; then
    echo "Usage: cybergis-script-env.sh geonode [install|reset]"
  else
    ENV=$1
    CMD=$2
    #
    if [[ "$CMD" = "install" ]]; then
      #
      bash --login -c "geonode_install"
      #
    elif [[ "$CMD" = "reset" ]]; then
      #
      source ~/.bash_aliases
      workon geonode
      source ~/.venvs/geonode/bin/activate
      #
      cd ~/geonode
      paver stop
      paver reset
      #paver reset_hard
      paver setup
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
      paver setup
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
  pip install pillow django-tastypie django-taggit django-jsonfield django-downloadview
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
    #
    if [[ "$CMD" = "install" ]]; then
      sudo apt-get update
      #
      sudo apt-get install -y python-software-properties
      sudo add-apt-repository ppa:chris-lea/node.js
      #
      sudo apt-get update
      #
      sudo apt-get install -y curl vim git
      #sudo apt-get install -y nodejs nodejs-dev npm
      #
      sudo npm config set registry http://registry.npmjs.org/
      sudo apt-get install -y nodejs nodejs-dev npm
      #
      sudo npm -g install grunt-cli karma bower
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
      sudo apt-get install postgresql-client-common postgresql-client-9.1 libgeos-dev
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
    
    if [[ $# -ne 2 ]]; then
        echo "Usage: cybergis-script-env.sh geonode [install|reset]"
    else
        export -f geonode_install
        export -f geonode
        bash --login -c "geonode $ENV $CMD"
    fi
    
elif [[ "$ENV" = "rogue" ]]; then
    
    if [[ $# -ne 2 ]]; then
        echo "Usage: cybergis-script-env.sh rogue [install|reset]"
    else
        export -f geonode_install
        export -f rogue
        bash --login -c "rogue $ENV $CMD"
    fi

elif [[ "$ENV" = "ittc" ]]; then
    
    if [[ $# -ne 2 ]]; then
        echo "Usage: cybergis-script-env.sh ittc [install|reset]"
    else
        export -f ittc
        bash --login -c "ittc $ENV $CMD"
    fi

else
    echo "Usage: cybergis-script-env.sh [geonode|ittc]"
fi
