from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse
import time
import os
import subprocess
import shutil

def clone_template(repo_url, repo_branch):
    #if not os.path.exists(path):
    #    os.makedirs(path)
    subprocess.call("git clone "+repo_url, cwd="/opt", shell=True)
    subprocess.call("git checkout -b "+repo_branch+" origin/"+repo_branch, cwd="/opt/rogue-chef-repo", shell=True)
    subprocess.call("git pull origin "+repo_branch, cwd="/opt/rogue-chef-repo", shell=True)
    
    if os.path.exists("/opt/chef-run"):
        shutil.rmtree("/opt/chef-run")

def create_chefrun(env):

    if not os.path.exists("/opt/chef-run"):
        os.makedirs("/opt/chef-run")
        
    print "Copying files into config directory /opt/chef-run/"
    
    subprocess.call("cp -r /opt/rogue-chef-repo/solo/* /opt/chef-run/;", cwd="/opt", shell=True)
    
    os.remove("/opt/chef-run/dna.json")
    os.remove("/opt/chef-run/dna_database.json")
    if not (env == "standalone"):
        os.remove("/opt/chef-run/dna_standalone.json")
    if not (env == "application"):
       os.remove("/opt/chef-run/dna_application.json")
    if not (env == "aws"):
        os.remove("/opt/chef-run/dna_aws.json")

    if env == "standalone":
        shutil.move("/opt/chef-run/dna_standalone.json", "/opt/chef-run/dna.json")
    if env == "application":
        shutil.move("/opt/chef-run/dna_application.json", "/opt/chef-run/dna.json")
    if env == "aws":
        shutil.move("/opt/chef-run/dna_aws.json", "/opt/chef-run/dna.json")

def build_dna_standalone(file_data, fqdn, gs_data_url, gs_data_branch, banner_on, banner_text, banner_color_text, banner_color_background):

    if file_data:
        data = None
        with open (file_data, "r") as f:
            data = f.read()
            data = data.replace('{{fqdn}}', fqdn)
            data = data.replace('{{gs-data-url}}', gs_data_url)
            data = data.replace('{{gs-data-branch}}', gs_data_branch)
            data = data.replace('{{banner-on}}', banner_on)
            data = data.replace('{{banner-text}}', banner_text)
            data = data.replace('{{banner-color-text}}', banner_color_text)
            data = data.replace('{{banner-color-background}}', banner_color_background)
                
        return data
    else:
        return None
        
def build_application(file_data, fqdn, gs_data_url, gs_data_branch, banner_on, banner_text, banner_color_text, banner_color_background, db_host, db_ip, db_port, db_user, db_pass):

    if file_data:
        data = None
        with open (file_data, "r") as f:
            data = f.read()
            data = data.replace('{{fqdn}}', fqdn)
            data = data.replace('{{gs-data-url}}', gs_data_url)
            data = data.replace('{{gs-data-branch}}', gs_data_branch)
            data = data.replace('{{banner-on}}', banner_on)
            data = data.replace('{{banner-text}}', banner_text)
            data = data.replace('{{banner-color-text}}', banner_color_text)
            data = data.replace('{{banner-color-background}}', banner_color_background)
            data = data.replace('{{db-host}}', db_host)
            data = data.replace('{{db-ip}}', db_ip)
            data = data.replace('{{db-port}}', db_port)
            data = data.replace('{{db-pass}}', db_pass)
                
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
    gs_data_url = args.gs_data_url
    gs_data_branch = args.gs_data_branch
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
    clone_template(repo_url, repo_branch)
    #==#
    create_chefrun(env)
    #==#
    if not fqdn:
        print "Missing FQDN"
        return 1
    if not (gs_data_url and gs_data_branch):
        print "Missing GeoServer data baseline"
        return 1
    if env == "application" or env=="aws":
        if not (db_host and db_ip and db_port and db_user and db_pass):
            print "Missing databse value"
            return 1
    #==#
    dna_path = "/opt/chef-run/dna.json"
    dna = None
    if env == "standalone":
        dna = build_dna_standalone(dna_path, fqdn, gs_data_url, gs_data_branch, banner_on, banner_text, banner_color_text, banner_color_background)
    elif env == "application":
        dna = build_application(dna_path, fqdn, gs_data_url, gs_data_branch, banner_on, banner_text, banner_color_text, banner_color_background, db_host, db_ip, db_port, db_user, db_pass)
    elif env == "aws":
        dna = build_application(dna_path, fqdn, gs_data_url, gs_data_branch, banner_on, banner_text, banner_color_text, banner_color_background, db_host, db_ip, db_port, db_user, db_pass)
    
    if dna:
        with open(dna_path, "w") as file:
            file.write(dna)

    print "=================================="
