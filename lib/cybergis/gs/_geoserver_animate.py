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
    export_s3 = args.s3
    #==#
    auth = None
    if args.username and args.password:
      auth = b64encode('{0}:{1}'.format(args.username, args.password))
    #==#
    aws_access_key_id = args.aws_access_key_id
    aws_secret_access_key = args.aws_secret_access_key
    #==#
    s3_overwrite = args.s3_overwrite
    s3_bucket = args.s3_bucket
    s3_key = args.s3_key
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
        if export_url > 0:
            print url

        if export_s3 > 0:
            if aws_access_key_id and aws_secret_access_key:
                if s3_bucket:
                    #==#
                    from boto.s3.connection import S3Connection
                    from boto.s3.key import Key
                    from PIL import Image
                    import io
                    #==#
                    s3 = S3Connection(aws_access_key_id, aws_secret_access_key)
                    bucket = s3.get_bucket(s3_bucket)
                    key = bucket.get_key(s3_key)
                    s3_go = False
                    if (not (key is None)) and key.exists():
                        if s3_overwrite > 0:
                            s3_go = True
                            bucket.delete_key(s3_key)
                            key = bucket.new_key(s3_key)
                        else:
                            print "Key already exists in bucket."
                    else:
                        key = bucket.new_key(s3_key)
                        s3_go = True

                    if s3_go and key:
                        fd = urllib.urlopen(url)
                        image = io.BytesIO(fd.read())
                        key.content_type = 'image/gif'
                        AWS_HEADERS = {'Cache-Control': str('no-cache, no-store, must-revalidate','Pragma':'no-cache','Expires':'0')}
                        key.update_metadata(AWS_HEADERS)
                        key.set_contents_from_file(image)
                else:
                    print "You need to specify an S3 Bucket"
            else:
                print "Missing AWS Credentials (Access Key ID and Secret Access Key)"

    except:
        print "Couldn't animate through layers "+args.layers+"."
        raise
    print "=================================="
