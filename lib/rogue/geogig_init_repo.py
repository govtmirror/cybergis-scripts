from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse
import time
import os

def make_request(url, params, auth=None, data=None):
    """
    Prepares a request from a url, params, and optionally authentication.
    """
    req = urllib2.Request(url + urllib.urlencode(params), data=data)

    if auth:
        req.add_header('AUTHORIZATION', 'Basic ' + auth)

    return urllib2.urlopen(req)

def parse_url(url):
    
    if (url is None) or len(url) == 0:
        return None
    
    index = url.rfind('/')

    if index != (len(url)-1):
        url += '/'
    
    return url

def createRepo(path):
    if not os.path.exists(path):
        os.makedirs(path)
    #subprocess.Popen("geogig init",cwd=repo)

def buildPOSTDataDataStore(name, path):
    file_data ="/opt/cybergis-scripts.git/lib/rogue/post_geogigdatastore.xml"
    data = None
    with open (file_data, "r") as f:
        data = f.read().replace('{{name}}', name).replace('{{path}}',path)
    return data

def createDataStore(geoserver, workspace, name, path):
    print('Creating GeoServer Datastore.')
    params = {'output_format': 'JSON'}
    data = buildPOSTDataDataStore(name, path)
    print data
    url = geoserver+"/workspaces/"+workspace+"/datastores.json"
    request = make_request(url=url+'?', params=params, auth=auth, data = data)

    if request.getcode() != 200:
        raise Exception("BeginTransaction failed: Status Code {0}".format(request.getcode()))

    response = json.loads(request.read())

    if not response['response']['success']:
        raise Exception("An error occurred on beginTransaction: {0}".format(response['response']['error']))

    print('Datastore created.')

    return transactionId;

#def getFeatureTypes(geoserver, repo):

#def createLayers(geoserver, repo):

def run(args):
    
    print args
    name = args.name 
    geoserver = parse_url(args.geoserver)
    path = args.path
    workspace = args.workspace
    #url_repo = geoserver+'geogig/'+repo+'/'
    
    auth = None
    if args.username and args.password:
      auth = b64encode('{0}:{1}'.format(args.username, args.password))

    print "=================================="
    print "#==#"
    print "CyberGIS Script / geogig_init_repo.py"
    print "Initialize GeoGig repository and optionally add to GeoServer instance."
    print "#==#"
    #Create GeoGig Repository and add to GeoServer
    createRepo(path)
    if args.geoserver and args.workspace and args.name:
        createDataStore(geoserver,workspace,name,path)

    return
    print "=================================="

parser = argparse.ArgumentParser(description='Initialize GeoGig repository and optionally add to GeoServer instance.')
parser.add_argument("path", help="The location in the filesystem of the Geogig repository.")
parser.add_argument("--name", help="The name of the GeoGig repo and data store in GeoServer.")
parser.add_argument("--geoserver", help="The url of the GeoServer servicing the GeoGig repository.")
parser.add_argument("--workspace", help="The GeoServer workspace to use for the data store.")
#parser.add_argument("--path", help="The location in the filesystem of the Geogig repository.")
parser.add_argument("--username", help="The username to use for basic auth requests.")
parser.add_argument("--password", help="The password to use for basic auth requests.")
  
args = parser.parse_args()
run(args)
