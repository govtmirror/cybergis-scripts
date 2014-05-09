#!/bin/bash
#This script is a work in development and is not stable.
#This script requires curl and git to be installed
#Run this script using rogue's login shell under: sudo su - <user>

if [[ $# -ne 2 ]]; then
	echo "Usage: cybergis-script-init.sh [rogue] [rvm|gems]"
	exit
fi

DATE=$(date)
RUBY_VERSION="2.0.0-p353"

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
}

if [[ "$1" -eq "rogue" ]]; then
    
    if [[ "$2" -eq "rvm" ]]; then
        export -f install_rvm
        bash -c init_user --login
    fi
    
    if [[ "$2" -eq "rvm" ]]; then
        export -f install_rvm
        bash -c install_rvm --login
    fi

    if [[ "$2" -eq "gems" ]]; then
        export -f install_gems
        bash -c install_gems --login
    fi
    
fi

