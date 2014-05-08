#!/bin/bash
#This script is a work in development and is not stable.
#This script requires curl and git to be installed
#Run this script using rogue's login shell under: sudo su - rogue

if [[ $# -ne 2 ]]; then
	echo "Usage: cybergis-script-configure-user-rogue.sh <fqdn> <user>"
	exit
fi

DATE=$(date)
FQDN=$1
USER=$2

install_gems(){
  #
  curl -L https://get.rvm.io | bash -s stable
  #
  rvm get stable
  rvm list known
  rvm install ruby-2.0.0-p35
  rvm --default use 2.0.0-p353
  ruby -v
  #
  gem install chef --version 11.8.0 --no-rdoc --no-ri --conservative
  gem install solve --version 0.8.2
  gem install nokogiri --version 1.6.1
  gem install berkshelf --version 2.0.14 --no-rdoc --no-ri
  gem list
}

#Load Functions
export -f install_gems

#Install Gems
su rogue -c "bash -c install_gems"
