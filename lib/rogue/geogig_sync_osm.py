from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse
import time
#==#
import _geogig_sync_osm
#==#
parser = argparse.ArgumentParser(description='Synchronize GeoGig repository with OpenStreetMap (OSM)')

parser.add_argument("update", default= 'true', help="true/false.  Update existing features only or download new features.  If false, extent and mapping are required.")

#
parser.add_argument("--workspace", help="The workspace of the GeoServer data store of the GeoGig repository you want to sync.")
parser.add_argument("--datastore", help="The name of the GeoServer data store of the GeoGig repository you want to sync.")
parser.add_argument("--repo", help="The GeoServer id of the GeoGig repository you want to sync.")

parser.add_argument("--geoserver", help="The url of the GeoServer servicing the GeoGig repository.")
parser.add_argument("--username", help="The username to use for basic auth requests.")
parser.add_argument("--password", help="The password to use for basic auth requests.")
parser.add_argument("--authorname", help="The author name to use when merging non-conflicting branches.")
parser.add_argument("--authoremail", help="The author email to use when merging non-conflicting branches.")
parser.add_argument("--extent", help="The extent of the OpenStreetMap extract. For example, basic:buildings_and_roads.")
parser.add_argument("--mapping", help="The mapping of the OpenStreetMap extract.  For example, dominican_republic:santo_domingo.")
parser.add_argument("--timeout", type=int, default=30, help="The number of seconds to wait for the osm download task to complete before cancelling.  Default is 30 seconds.")
parser.add_argument('--verbose', '-v', default=0, action='count', help="Print out intermediate status messages.")
args = parser.parse_args()
#==#
_geogig_sync_osm.run(args)
