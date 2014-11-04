from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse
import time
import os
import subprocess

def buildDNA(env, fqdn, db_host, db_ip, db_port, db_pass, gs_baseline, banner_text, banner_color_text, banner_color_background):
    
    file_data = None
    if env == "standalone":
        file_data ="/opt/chef-run/dna/dna_standalone.json"
    elif env == "aws":
        file_data ="/opt/chef-run/dna/dna_aws.json"
    elif env == "application":
        file_data ="/opt/chef-run/dna/dna_application.json"
    
    if file_data:
        data = None
        with open (file_data, "r") as f:
            data = f.read()
                .replace('{{fqdn}}', fqdn)
                .replace('{{db_host}}', db_host)
                .replace('{{db_ip}}', db_ip)
                .replace('{{db_port}}', db_port)
                .replace('{{db_pass}}', db_pass)
                .replace('{{gs_baseline}}', gs_baseline)
                .replace('{{banner_text}}', banner_text)
                .replace('{{banner_color_text}}', banner_color_text)
                .replace('{{banner_color_background}}', banner_color_background)
        return data
    else:
        return None

def run(args):
    #print args
    #==#
    verbose = args.verbose
    #==#

    #==#

    #==#

    #==#

    #==#
    print "=================================="
    print "#==#"
    print "CyberGIS Script / cybergis-script-geoshape-configure.py"
    print "Configure GeoSHAPE instance"
    print "#==#"
    #==#
                    
    print "=================================="
