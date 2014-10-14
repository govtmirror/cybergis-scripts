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
    print url + urllib.urlencode(params)
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

    
def buildPOSTDataLayerGroup(layergroup, layers, styles):
    data = "<layerGroup><name>"+layergroup+"</name>"
    data += "<layers>"
    for layer in layers:
        data += "<layer>"+layer+"</layer>"
    data += "</layers>"
    if styles:
        data += "<styles>"
        for style in styles:
            data += "<style>"+style+"</style>"
        data += "</styles>"
    data +="</layerGroup>"
    return data

def createLayerGroup(verbose, geoserver, workspace, auth, layergroup, layers, styles):
    if verbose > 0:
        print('Creating GeoServer Layergroup for '+layergroup+".")
    params = {}
    data = buildPOSTDataLayerGroup(layergroup, layers, styles)
    url = geoserver+"rest/workspaces/"+workspace+"/layergroups.xml"
    
    try:
        request = make_request(url=url+'?', params=params, auth=auth, data=data)
    except:
        #raise Exception("Create layergroup failed with url="+url+", params="+str(params)+", data="+data)
        print "Create layergroup failed with url="+url+", params="+str(params)+", data="+data
        raise

    if request.getcode() != 201:
        raise Exception("Create layergroup failed: Status Code {0}".format(request.getcode()))
        
    if verbose > 0:
        print('Layer created.')
        
def parse_layers(layers):
    if layers and len(layers) > 0:
        try:
            return layers.split(",")
        except:
            return None
    else:
        return None

def parse_styles(styles):
    if styles and len(styles) > 0:
        try:
            return styles.split(",")
        except:
            return None
    else:
        return None

def run(args):
    #print args
    #==#
    verbose = args.verbose
    #==#
    layers = parse_layers(args.layers)
    styles = parse_styles(args.styles)
    geoserver = parse_url(args.geoserver)
    workspace = args.workspace
    layergroup = args.layergroup
    #==#
    auth = None
    if args.username and args.password:
      auth = b64encode('{0}:{1}'.format(args.username, args.password))
    #==#
    print "=================================="
    print "#==#"
    print "CyberGIS Script / cybergis-scrit-geoserver-publish-layergroup.py"
    print "Publishes multiple layers as a layer group"
    print "#==#"
    #==#
    if not layers:
        print "Could not parse layers correctly."
        return 1
    
    if styles:
        if len(styles) != len(layers):
            print "Layers and styles arrays do not have the same length."
            return 1
    #==#
    #Publish Layers as Layer Group
    try:
        createLayerGroup(verbose, geoserver, workspace, auth, layergroup, layers, styles)
    except:
        print "Couldn't create layergroup from layers "+args.layers+"."
        raise
    print "=================================="
