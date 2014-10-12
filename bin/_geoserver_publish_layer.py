from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse
import time
import os
import subprocess

def make_request(url, params, auth=None, data=None, contentType=None):
    """
    Prepares a request from a url, params, and optionally authentication.
    """
    req = urllib2.Request(url + urllib.urlencode(params), data=data)

    if auth:
        req.add_header('AUTHORIZATION', 'Basic ' + auth)
    
    if contentType:
        req.add_header('Content-type', contentType)
    else:
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
    table = args.table
    datastore = args.datastore
    geoserver = parse_url(args.geoserver)
    workspace = args.workspace
    #==#
    auth = None
    if args.username and args.password:
      auth = b64encode('{0}:{1}'.format(args.username, args.password))
    #==#
    print "=================================="
    print "#==#"
    print "CyberGIS Script / cybergis-scrit-geoserver-publish-layer.py"
    print "Publish PostGIS Table as Layer"
    print "#==#"
    #==#
    #Publish PostGIS Table as Layer
    try:
        createLayer(verbose, geoserver, workspace, auth, datastore, table)
    except:
        print "Couldn't create layer from PostGIS data store "+datastore+" for table "+table+"."
    print "=================================="
