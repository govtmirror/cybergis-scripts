#!/bin/bash
#This script is a work in development and is not stable.
#This script requires curl and git to be installed
#Run this script using root's login shell under: sudo su -

DATE=$(date)

ENV=$1

#==================================#

geonode(){
  echo "geonode"
  if [[ $# -ne 1 ]]; then
    echo "Usage: cybergis-script-env.sh geonode"
  else
    ENV=$1
    #
    sudo apt-get update
    # Essential build tools and libraries
    sudo apt-get install -y build-essential libxml2-dev libxslt1-dev libjpeg-dev gettext git python-dev python-pip python-virtualenv
    # Python and Django dependencies with official packages
    sudo apt-get install -y python-lxml python-psycopg2 python-django python-bs4 python-multipartposthandler transifex-client python-nose python-django-nose python-gdal python-django-pagination python-django-extensions python-httplib2
    # Java dependencies
    sudo apt-get install -y --force-yes openjdk-6-jdk ant maven2 --no-install-recommends
    #Install python packages for development
    sudo pip install virtualenvwrapper paver
    
    #Add all these lines to ~/.bash_aliases
    echo 'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python' >> ~/.bash_alises
    echo 'export WORKON_HOME=~/.venvs' >> ~/.bash_alises
    echo 'source /usr/local/bin/virtualenvwrapper.sh'>> ~/.bash_alises
    echo 'export PIP_DOWNLOAD_CACHE=$HOME/.pip-downloads' >> ~/.bash_alises
    echo 'workon geonode' >> ~/.bash_alises
    
    cd ~/geonode
    mkvirtualenv geonode
    workon geonode
    pip install pillow django-taggit django-jsonfield
    #Install GeoNode
    pip install -e geonode
    #cd geonode
    #./restart.sh
    
  fi
}

if [[ "$ENV" = "geonode" ]]; then
    
    if [[ $# -ne 3 ]]; then
        echo "Usage: cybergis-script-env.sh geonode"
    else
        export -f geonode
        bash --login -c geonode
    fi

else
    echo "Usage: cybergis-script-env.sh [geonode]"
fi
