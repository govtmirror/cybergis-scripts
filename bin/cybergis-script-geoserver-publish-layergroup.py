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
import gs._geoserver_publish_layergroup
#==#
parser = argparse.ArgumentParser(description='')
#==#
parser.add_argument('-gs', '--geoserver', help="The url of the target GeoServer.")
parser.add_argument('-ws', '--workspace', help="The GeoServer workspace to use for the data store.")
#==#
parser.add_argument('-lg','--layergroup', help="The name of the new layer group.")
parser.add_argument('--layers', help="The layers comma-separated in GeoServer to be combined into the layer group.")
#==#
parser.add_argument("--username", help="The username to use for basic auth requests.")
parser.add_argument("--password", help="The password to use for basic auth requests.")
#==#
parser.add_argument('--verbose', '-v', default=0, action='count', help="Print out intermediate status messages.")
args = parser.parse_args()
#==#
gs._geoserver_publish_layergroup.run(args)
