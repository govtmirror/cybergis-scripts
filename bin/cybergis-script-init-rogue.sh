#!/bin/bash
#This script is a work in development and is not stable.
#This script requires curl and git to be installed
#Run this script using rogue's login shell under: sudo su - <user>

if [[ $# -ne 2 ]]; then
	echo "Usage: cybergis-script-init-rogue.sh [prod|dev] [user|rvm|gems|geonode]"
	exit
fi

DATE=$(date)
RUBY_VERSION="2.0.0-p353"

INIT_ENV=$1
INIT_CMD=$2

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
  #
  #cd /opt/
  #git clone https://github.com/ROGUE-JCTD/rogue-chef-repo.git
  #mkdir chef-run
  #cp -r /opt/rogue-chef-repo/solo/* chef-run/
  #cd /opt/chef-run
  #cd /opt/rogue-chef-repo
  #source /home/rogue/.rvm/scripts/rvm
  #type rvm | head -1
  #git pull
  #berks update
  #berks install --path /opt/chef-run/cookbooks
  #
  #rvmsudo chef-solo -c /opt/chef-run/solo.rb -j /opt/chef-run/dna.json
  #
}

if [[ "$INIT_ENV" = "prod" ]]; then
    
    if [[ "$INIT_CMD" == "user" ]]; then
        export -f init_user
        bash -c init_user --login
    fi
    
    if [[ "$INIT_CMD" == "rvm" ]]; then
        export -f install_rvm
        bash -c install_rvm --login
    fi

    if [[ "$INIT_CMD" == "gems" ]]; then
        export -f install_gems
        bash -c install_gems --login
    fi
    
    if [[ "$INIT_CMD" == "geonode" ]]; then
        export -f install_geonode
        bash -c install_geonode --login
    fi
    
fi

