#!/usr/bin/python
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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib', 'cybergis')))
import gs._geoserver_animate
#==#
parser = argparse.ArgumentParser(description='')
#==#
parser.add_argument('-gs', '--geoserver', help="The url of the target GeoServer.")
#==#
parser.add_argument('--layers', help="The layers to animate through.")
parser.add_argument('--srs', default="4326", help="The SRS, such as 4326, 900913, etc.")
parser.add_argument('--bbox', help="The bounding box to animate against.")
#==#
parser.add_argument('--width', help="The width of the output animated GIF in pixels.  These should be compatible with the bounding box.")
parser.add_argument('--height', help="The height of the output animated GIF in pixels.  This should be compatible with the bounding box.")
#==#
parser.add_argument("--username", help="The username to use for basic auth requests.")
parser.add_argument("--password", help="The password to use for basic auth requests.")
#==#
parser.add_argument('--verbose', '-v', default=0, action='count', help="Print out intermediate status messages.")
#==#
parser.add_argument('--url', default=0, action='count', help="Display url to animated GIF")
parser.add_argument('--file', default=0, action='count', help="Export animated GIF to file.")
parser.add_argument('--s3', default=0, action='count', help="Upload animation directly to AWS S3.")
#==#
parser.add_argument('--aws_access_key_id', help="AWS API Key ID.")
parser.add_argument('--aws_secret_access_key', help="AWS API Key Secret.")
parser.add_argument('--s3_overwrite', help="Overwrite object in S3 if it already exists.")
parser.add_argument('--s3_bucket', help="The AWS S3 Bucket to upload the animation")
parser.add_argument('--s3_key', help="The AWS S3 Key for the animation (filename).")
#==#
args = parser.parse_args()
#==#
gs._geoserver_animate.run(args)
