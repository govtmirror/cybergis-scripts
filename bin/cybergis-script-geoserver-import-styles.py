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
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
from ..lib import cybergis.gs
#==#
parser = argparse.ArgumentParser(description='')
parser.add_argument("--path", help="The location in the filesystem of the styles directory")
parser.add_argument("--prefix", help="The prefix to prepend to all the styles when loaded into GeoServer")
parser.add_argument('-gs', '--geoserver', help="The url of the target GeoServer.")
parser.add_argument("--username", help="The username to use for basic auth requests.")
parser.add_argument("--password", help="The password to use for basic auth requests.")
parser.add_argument('--verbose', '-v', default=0, action='count', help="Print out intermediate status messages.")
args = parser.parse_args()
#==#
cybergis.gs._geoserver_import_styles.run(args)
