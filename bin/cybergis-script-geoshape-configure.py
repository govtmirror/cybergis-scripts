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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib', 'cybergis')))
import geoshape._geoshape_configure
#==#
parser = argparse.ArgumentParser(description='Initialize GeoGig repository and optionally add to GeoServer instance.  If you want to add the GeoGig repo include the optional parameters.')
#==#
parser.add_argument('--verbose', '-v', default=0, action='count', help="Print out intermediate status messages.")
#==#
parser.add_argument("--env", default="standalone", help="The environment (standalone, application, or aws).")
#==#
parser.add_argument("--fqdn", default="localhost", help="The fqdn of GeoSHAPE.")
#==#
parser.add_argument("--gs_baseline", default="master", help="The baseline geoserver_data version.")
#==#
parser.add_argument('--banner', default=0, action='count', help="Display a banner")
parser.add_argument("--banner_text", help="The banner text.")
parser.add_argument("--banner_color_text", help="The foreground/font color of the banner text.")
parser.add_argument("--banner_color_background", help="The background color of the banner.")
#==#
#When env equals application or aws
parser.add_argument("--db_host", help="The database host")
parser.add_argument("--db_ip", help="The database ip")
parser.add_argument("--db_port", default="5432", help="The database port")
parser.add_argument("--db_user", default="postgres", help="The database user")
parser.add_argument("--db_pass", help="The database password")
#==#
args = parser.parse_args()
#==#
geoshape._geoshape_configure.run(args)
