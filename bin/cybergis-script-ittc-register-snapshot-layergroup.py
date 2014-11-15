#!/usr/bin/python
from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse
import time
import sys
import os
import subprocess
#==#
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib', 'cybergis')))
import gs._geoserver_animate
#==#
parser = argparse.ArgumentParser(description='')
#==#
parser.add_argument("--db_host", help="The database host.")
parser.add_argument("--db_port", default="5432", help="The database port.")
parser.add_argument("--db_name", default="ittc_snapshots_1", help="The database name with the snapshot table.")
#==#
parser.add_argument("--username", default="postgres", help="The username to access the database.")
parser.add_argument("--password", help="The password to access the database.")
#==#
parser.add_argument('--table', help="The layergroup snapshot table.")
#==#
parser.add_argument('--source_name', help="The source designator.")
parser.add_argument('--source_layers', help="The source layers.")
parser.add_argument('-ts', '--timestamp', help="The timestamp of the snapshot.")
parser.add_argument('--snapshot_layergroup', help="The new snapshot layergroup.")
#==#
parser.add_argument('--verbose', '-v', default=0, action='count', help="Print out intermediate status messages.")
#==#
args = parser.parse_args()
#==#
gs._geoserver_animate.run(args)
