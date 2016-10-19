#!/usr/bin/python
from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse
import time
import os
import sys
#==#
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib', 'cybergis')))
import ittc._ittc_stretch
#==#
parser = argparse.ArgumentParser(description='Apply stetch to raster image(s).')
#
parser.add_argument("input", help="Path to input image file(s)")
parser.add_argument("breakpoints", help="Path to breakpoints file")
parser.add_argument("output", help="Path to output image file")
parser.add_argument("bands", help="The number of bands to stretch.  This is not inferred.  You need to be explicit.  Most likely 1 or 3.")
#
parser.add_argument('-r', '--rows', default='256', help="The number of rows to load into memory at a time to stretch.  Default = 256.")
parser.add_argument('-t', '--threads', default='1', help="The maximum number of threads to activate.  Default = 1.")
#
parser.add_argument('--verbose', '-v', default=0, action='count', help="Print out intermediate status messages.")
parser.add_argument('--force', '-f', default=0, action='count', help="Force.  Replace existing output file if exists.")
#
args = parser.parse_args()
#==#
ittc._ittc_stretch.run(args)
