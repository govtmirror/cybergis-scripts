from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse
import time
import os
import subprocess

def make_request(url, params, auth=None, data=None):
    """
    Prepares a request from a url, params, and optionally authentication.
    """
    req = urllib2.Request(url + urllib.urlencode(params), data=data)

    if auth:
        req.add_header('AUTHORIZATION', 'Basic ' + auth)
    if data:
        req.add_header('Content-type', 'text/xml')

    return urllib2.urlopen(req)

def parse_url(url):
    
    if (url is None) or len(url) == 0:
        return None
    
    index = url.rfind('/')

    if index != (len(url)-1):
        url += '/'
    
    return url

    
def buildPOSTDataLayer(name,nativeName,title):
    file_data ="/opt/cybergis-scripts.git/templates/post_postgis_layer.xml"
    data = None
    with open (file_data, "r") as f:
        data = f.read().replace('{{name}}', name).replace('{{nativeName}}', nativeName).replace('{{title}}', title)
    return data

def createLayer(verbose, geoserver, workspace, auth, datastore, layer):
    if verbose > 0:
        print('Creating GeoServer Layer for '+layer+".")
    params = {}
    data = buildPOSTDataLayer(datastore+"_"+layer,layer,datastore+"_"+layer)
    url = geoserver+"rest/workspaces/"+workspace+"/datastores/"+datastore+"/featuretypes.xml"
    
    try:
        request = make_request(url=url+'?', params=params, auth=auth, data=data)
    except:
        raise Exception("Create layer failed: Status Code {0}".format(request.getcode()))

    if request.getcode() != 201:
        raise Exception("Create layer failed: Status Code {0}".format(request.getcode()))
        
    if verbose > 0:
        print('Layer created.')

def run(args):
    #print args
    #==#
    verbose = args.verbose
    #==#
    publish_datastore = args.publish_datastore
    publish_layers = args.publish_layers
    #==#
    name = args.name
    datastore = name
    geoserver = parse_url(args.geoserver)
    path = args.path
    workspace = args.workspace
    #url_repo = geoserver+'geogig/'+repo+'/'
    #==#
    auth = None
    if args.username and args.password:
      auth = b64encode('{0}:{1}'.format(args.username, args.password))
    #==#
    print "=================================="
    print "#==#"
    print "CyberGIS Script / geogig_init_repo.py"
    print "Initialize GeoGig repository and optionally add to GeoServer instance."
    print "#==#"
    #==#
    #Publish PostGIS Table as Layer
    if publish_layers > 0:
        try:
            createLayer(verbose, geoserver, workspace, auth, datastore, tree)
        except:
            print "Couldn't create layer from datastore "+datastore+" for tree "+tree+"."
    print "=================================="
