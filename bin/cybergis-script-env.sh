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
    apt-get update
    # Essential build tools and libraries
    apt-get install -y build-essential libxml2-dev libxslt1-dev libjpeg-dev gettext git python-dev python-pip
    # Python and Django dependencies with official packages
    apt-get install -y  python-lxml python-psycopg2 python-django python-bs4 python-multipartposthandler transifex-client python-nose python-django-nose python-gdal python-django-pagination python-django-extensions python-httplib2
    # Java dependencies
    apt-get install -y --force-yes openjdk-6-jdk ant maven2 --no-install-recommends

    pip install python-pillow python-paver python-django-taggit python-django-jsonfield 
    

    #Add all these lines to ~/.bash_aliases
    echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
export WORKON_HOME=~/.venvs
source /usr/local/bin/virtualenvwrapper.sh
export PIP_DOWNLOAD_CACHE=$HOME/.pip-downloads
workon geonode
"
    

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
