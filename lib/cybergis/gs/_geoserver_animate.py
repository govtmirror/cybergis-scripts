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

    
def buildQueryString(layers, srs, bbox, width, height):
    qs = {
        "FORMAT": "image/gif;subtype=animated",
        "format_options": "gif_loop_continuosly:true",
        "aparam": "layers",
        "SRS": "EPSG:"+srs,
        "BBOX": bbox,
        "WIDTH": width,
        "HEIGHT": height,
        "avalues": (",".join(layers))
    }
    return urllib.urlencode(qs)

    #qs += "FORMAT=image/gif;subtype=animated&format_options=gif_loop_continuosly:true&aparam=layers"
    #qs += "&SRS=EPSG%3A900913"
    #qs += "&BBOX="+bbox
    #qs += "&WIDTH="+width
    #qs += "&HEIGHT="+height
    #qs += "&avalues="+(",".join(layers))

    #return qs

def buildURL(geoserver, layers, srs, bbox, width, height):
    if geoserver:
        qs = buildQueryString(layers, srs, bbox, width, height)
        return geoserver + "wms/animate?" + qs
    else:
        return None

def parse_layers(layers):
    if layers and len(layers) > 0:
        try:
            return layers.split(",")
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
    geoserver = parse_url(args.geoserver)
    #==#
    width = args.width
    height = args.height
    #==#
    srs = args.srs
    bbox = args.bbox
    #==#
    export_url = args.url
    export_file = args.file
    #==#
    auth = None
    if args.username and args.password:
      auth = b64encode('{0}:{1}'.format(args.username, args.password))
    #==#
    print "=================================="
    print "#==#"
    print "CyberGIS Script / cybergis-scrit-geoserver-animate.py"
    print "Animate through list of layers for a given bounding box"
    print "#==#"
    #==#
    if not layers:
        print "Could not parse layers correctly."
        return 1
    
    #==#
    #Animate through layers
    try:
        url = buildURL(geoserver, layers, srs, bbox, width, height)
        if export_url:
            print url
    except:
        print "Couldn't animate through layers "+args.layers+"."
        raise
    print "=================================="
