from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse
import time
import os
import subprocess

def install_dependencies():
    print "If the server stalls on installing GEMS, run <source /usr/local/rvm/scripts/rvm; gem install dep-selector-libgecode -v '1.0.2'> from the command line and then run again."
    #subprocess.Popen("source /usr/local/rvm/scripts/rvm; bundle install; berks install", cwd=path, shell=True)
    p = subprocess.Popen("source /usr/local/rvm/scripts/rvm; bundle install; berks install;", shell=True)
    #time.sleep(5)
    print "Waiting for dependencies to finish installing"
    p.communicate()
    
def clone_template(repo_url, repo_branch):
    #if not os.path.exists(path):
    #    os.makedirs(path)
    subprocess.call("git clone "+repo_url, cwd="/opt", shell=True)
    subprocess.call("git checkout -b "+repo_branch+" origin/"+repo_branch, cwd="/opt/rogue-chef-repo", shell=True)
    subprocess.call("git pull origin "+repo_branch, cwd="/opt/rogue-chef-repo", shell=True)
    
    if os.path.exists("/opt/chef-run"):
        os.remove("/opt/chef-run")

def create_chefrun():
    if not os.path.exists("/opt/chef-run"):
        os.mkdirs("/opt/chef-run")
    print "Copying files into config directory /opt/chef-run/"
    
    mkdir /opt/chef-run
    echo "Copying files into config directory /opt/chef-run/"
    cp -r /opt/rogue-chef-repo/solo/* /opt/chef-run/
    cd /opt/chef-run
    rm dna.json
    rm dna_database.json
    rm dna_standalone.json
    rm dna_application.json
    mv dna_aws.json dna.json


def build_dna_standalone(file_data, fqdn, gs_baseline, banner_on, banner_text, banner_color_text, banner_color_background):

    if file_data:
        data = None
        with open (file_data, "r") as f:
            data = f.read()
                .replace('{{fqdn}}', fqdn)
                .replace('{{gs_baseline}}', gs_baseline)
                .replace('{{banner_on}}', banner_on)
                .replace('{{banner_text}}', banner_text)
                .replace('{{banner_color_text}}', banner_color_text)
                .replace('{{banner_color_background}}', banner_color_background)
                
        return data
    else:
        return None
        
def build_application(file_data, fqdn, gs_baseline, banner_on, banner_text, banner_color_text, banner_color_background, db_host, db_ip, db_port, db_user, db_pass):

    if file_data:
        data = None
        with open (file_data, "r") as f:
            data = f.read()
                .replace('{{fqdn}}', fqdn)
                .replace('{{gs_baseline}}', gs_baseline)
                .replace('{{banner_on}}', banner_on)
                .replace('{{banner_text}}', banner_text)
                .replace('{{banner_color_text}}', banner_color_text)
                .replace('{{banner_color_background}}', banner_color_background)
                .replace('{{db_host}}', db_host)
                .replace('{{db_ip}}', db_ip)
                .replace('{{db_port}}', db_port)
                .replace('{{db_pass}}', db_pass)
                
        return data
    else:
        return None

def run(args):
    #print args
    #==#
    verbose = args.verbose
    #==#
    env = args.env
    repo_url = args.repo_url
    repo_branch = args.repo_branch
    #==#
    fqdn = args.fqdn
    gs_baseline = args.gs_baseline
    #==#
    banner_on = "true" if args.banner == 1 else "false"
    banner_text = args.banner_text
    banner_color_text = args.banner_color_text
    banner_color_background = args.banner_color_background
    #==#
    db_host = args.db_host
    db_ip = args.db_ip
    db_port = args.db_port
    db_user = args.db_user
    db_pass = args.db_pass
    #==#
    print "=================================="
    print "#==#"
    print "CyberGIS Script / cybergis-script-geoshape-configure.py"
    print "Configure GeoSHAPE instance"
    print "#==#"
    #==#
    install_dependencies()
    #==#
    clone_template(repo_url, repo_branch)
    #==#
    file_data = None
    if env == "standalone":
        file_data ="/opt/chef-run/dna/dna_standalone.json"
    elif env == "aws":
        file_data ="/opt/chef-run/dna/dna_aws.json"
    elif env == "application":
        file_data ="/opt/chef-run/dna/dna_application.json"                
    print "=================================="
