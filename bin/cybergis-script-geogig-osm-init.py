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
import gg._geogig_init_repo
import gg._geogig_sync_osm
#==#
class ov(object):
    def __init__(self, d):
        self.__dict__ = d
        
def run(args):
    #print args
    #==#
    verbose = args.verbose
    #==
    authorname = args.authorname
    authoremail = args.authoremail
    #==#
    name = args.name
    geoserver = args.geoserver
    path = args.path
    workspace = args.workspace
    timeout = args.timeout
    #==#
    username = args.username
    password = args.password
    #==#
    extent = args.extent
    mapping = args.mapping
    #==#
    print "=================================="
    print "#==#"
    print "CyberGIS Script / geogig_init_extract.py"
    print "Initialize GeoGig repository, adds to GeoServer, downloads OSM extract, publishes layers"
    print "#==#"
    #==#
    print "Executing subroutines"
    gg._geogig_init_repo.run(ov({
        'path': path,
        'name': name,
        'geoserver': geoserver,
        'workspace': workspace,
        'publish_datastore': 1,
        'publish_layers': 0,
        'username': username,
        'password': password,
        'verbose': verbose
    }))
    #==#
    gg._geogig_sync_osm.run(ov({
        'update': 'false',
        'repo':None,
        'datastore': name,
        'geoserver': geoserver,
        'workspace': workspace,
        'username': username,
        'password': password,
        'verbose': verbose,
        'authorname':authorname,
        'authoremail': authoremail,
        'extent': extent,
        'mapping': mapping,
        'timeout': timeout
    }))
    #==#
    gg._geogig_init_repo.run(ov({
        'path': None,
        'name': name,
        'geoserver': geoserver,
        'workspace': workspace,
        'publish_datastore': 0,
        'publish_layers': 1,
        'username': username,
        'password': password,
        'verbose': verbose
    }))                    
    print "=================================="

parser = argparse.ArgumentParser(description='Initialize GeoGig repository and optionally add to GeoServer instance.  If you want to add the GeoGig repo include the optional parameters.')
parser.add_argument("--path", help="The location in the filesystem of the Geogig repository.")
parser.add_argument("--name", help="The name of the GeoGig repo and data store in GeoServer.")
parser.add_argument('-gs', '--geoserver', help="The url of the GeoServer servicing the GeoGig repository.")
parser.add_argument('-ws', '--workspace', help="The GeoServer workspace to use for the data store.")
parser.add_argument("--username", help="The username to use for basic auth requests.")
parser.add_argument("--password", help="The password to use for basic auth requests.")
parser.add_argument('--verbose', '-v', default=0, action='count', help="Print out intermediate status messages.")
parser.add_argument('-an', '--authorname', help="The author name to use when merging non-conflicting branches.")
parser.add_argument('-ae', '--authoremail', help="The author email to use when merging non-conflicting branches.")
parser.add_argument("--extent", help="The extent of the OpenStreetMap extract. For example, basic:buildings_and_roads.")
parser.add_argument("--mapping", help="The mapping of the OpenStreetMap extract.  For example, dominican_republic:santo_domingo.")
parser.add_argument('-to', '--timeout', type=int, default=30, help="The number of seconds to wait for the osm download task to complete before cancelling.  Default is 30 seconds.")
args = parser.parse_args()
#==#
run(args)
