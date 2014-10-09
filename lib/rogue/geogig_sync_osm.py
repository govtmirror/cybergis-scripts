from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse

parser = argparse.ArgumentParser(description='Synchronize GeoGig repository with OpenStreetMap (OSM)')
parser.add_argument("url", help="The url to the repository you want to sync.")
parser.add_argument("--username", help="The username to use for basic auth requests.")
parser.add_argument("--password", help="The password to use for basic auth requests.")
parser.add_argument("authorname", help="The author name to use when merging non-conflicting branches.")
parser.add_argument("authoremail", help="The author email to use when merging non-conflicting branches.")
args = parser.parse_args()

print args.accumulate(args.integers)
