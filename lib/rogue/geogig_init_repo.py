from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse
import time
import os
import subprocess
#==#
import _geogig_init_repo
#==#
parser = argparse.ArgumentParser(description='Initialize GeoGig repository and optionally add to GeoServer instance.  If you want to add the GeoGig repo include the optional parameters.')
parser.add_argument("--path", help="The location in the filesystem of the Geogig repository.")
parser.add_argument("--name", help="The name of the GeoGig repo and data store in GeoServer.")
parser.add_argument('-gs', '--geoserver', help="The url of the GeoServer servicing the GeoGig repository.")
parser.add_argument('-ws', '--workspace', help="The GeoServer workspace to use for the data store.")
#parser.add_argument("--path", help="The location in the filesystem of the Geogig repository.")
parser.add_argument("--username", help="The username to use for basic auth requests.")
parser.add_argument("--password", help="The password to use for basic auth requests.")
parser.add_argument('--verbose', '-v', default=0, action='count', help="Print out intermediate status messages.")
parser.add_argument("--publish_datastore", default=0, action='count', help="Publish datastore in GeoServer for GeoGig repository")
parser.add_argument('--publish_layers', default=0, action='count', help="Publish layers from GeoGig data store")
args = parser.parse_args()
#==#
_geogig_init_repo.run(args)
