from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse

def make_request(url, params, auth=None):
    """
    Prepares a request from a url, params, and optionally authentication.
    """
    req = urllib2.Request(url + urllib.urlencode(params))

    if auth:
        req.add_header('AUTHORIZATION', 'Basic ' + auth)

    return urllib2.urlopen(req)

def beginTransaction(url, auth):
    print('Starting transaction...')
    params = {'output_format': 'JSON'}
    request = make_request(url=url+'beginTransaction.json?', params=params, auth=auth)

    if request.getcode() != 200:
        raise Exception("BeginTransaction failed: Status Code {0}".format(request.getcode()))
        
    response = json.loads(request.read())

    if not response['response']['success']:
        raise Exception("An error occurred on beginTransaction: {0}".format(response['response']['error']))

    print('Transaction started')
    transactionId = response['response']['Transaction']['ID']
        
    return transactionId;

def endTransaction(url, auth, cancel, transactionId):
    print('Ending transaction...')
    params = {'output_format': 'JSON', 'cancel': cancel, 'transactionId': transactionId}
    request = make_request(url=url+'endTransaction.json?', params=params, auth=auth)

    if request.getcode() != 200:
        raise Exception("EndTransaction failed: Status Code {0}".format(request.getcode()))
    
    response = json.loads(request.read())
    
    if not response['response']['success']:
        raise Exception("An error occurred on endTransaction: {0}".format(response['response']['error']))

def downloadFromOSM(url, auth, transactionId):
    print('Downloading from OpenStreetMap ...')
    params = {'output_format': 'JSON', 'update': 'true'}
    request = make_request(url=url+'osm/download.json?', params=params, auth=auth)

    if request.getcode() != 200:
        raise Exception("OSM Download failed: Status Code {0}".format(request.getcode()))
        
    response = json.loads(request.read())

    if not response['response']['success']:
        raise Exception("An error occurred when pulling new data from OSM: {0}".format(response['response']['error']))

    print('Download from OpenStreetMap complete.')
 
def parse_url(args):
    url = args.url
    
    if (url is None) or len(url) == 0:
        return None
    
    index = url.rfind('/')

    if index != (len(url)-1):
        url += '/'
    
    return url

def run(args):
    url = parse_url(args)
    if url is None:
        print "Please specify a url"
        return 1
        
    authorname = args.authorname
    authoremail = args.authoremail
    auth = None
    if args.username and args.password:
      auth = b64encode('{0}:{1}'.format(args.username, args.password))

    transactionId = -1
    try:
        transactionId = beginTransaction(url, auth)
    except Exception:
        transactionId = -1
        raise
    
    if transactionId != -1:
        try:
            downloadFromOSM(url, auth, transactionId)
        except Exception:
            endTransaction(url, auth, True, transactionId)
            raise
    
    try:
        endTransaction(url, auth, False, transactionId)
    except Exception:
        pass

parser = argparse.ArgumentParser(description='Synchronize GeoGig repository with OpenStreetMap (OSM)')
parser.add_argument("url", help="The url to the repository you want to sync.")
parser.add_argument("--username", help="The username to use for basic auth requests.")
parser.add_argument("--password", help="The password to use for basic auth requests.")
parser.add_argument("--authorname", help="The author name to use when merging non-conflicting branches.")
parser.add_argument("--authoremail", help="The author email to use when merging non-conflicting branches.")
  
args = parser.parse_args()
run(args)
