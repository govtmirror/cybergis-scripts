from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse

def beginTransaction(url, auth):
    params = {'output_format': 'JSON'}
    self.stdout.write('Starting transaction...')
    request = self.make_request(url=url+'beginTransaction?', params=params, auth=auth)

    if request.getcode() != 200:
        raise Exception("BeginTransaction failed: Status Code {0}".format(request.getcode()))
        
    response = json.loads(request.read())

    if not response['response']['success']:
        raise Exception("An error occurred on beginTransaction: {0}".format(response['response']['error']))

    self.stdout.write('Transaction started')
    transactionId = response['response']['Transaction']['ID']
        
    return transactionId;

def endTransaction(url, auth, cancel, transactionId):
    params = {'output_format': 'JSON', 'cancel': cancel, 'transactionId': transactionId}
    request = self.make_request(url=url+'endTransaction?', params=params, auth=auth)

    if request.getcode() != 200:
        raise Exception("EndTransaction failed: Status Code {0}".format(request.getcode()))
    
    response = json.loads(request.read())
    
    if not response['response']['success']:
        raise Exception("An error occurred on endTransaction: {0}".format(response['response']['error']))

def pullFromOSM(url, auth, transactionId):
    params = {'output_format': 'JSON', 'update': 'true'}
    self.stdout.write('Starting transaction...')
    request = self.make_request(url=url+'osm/download.xml?', params=params, auth=auth)

    if request.getcode() != 200:
        raise Exception("OSM Download failed: Status Code {0}".format(request.getcode()))
        
    response = json.loads(request.read())

    if not response['response']['success']:
        raise Exception("An error occurred when pulling new data from OSM: {0}".format(response['response']['error']))

    self.stdout.write('Pull from OSM complete.')
 
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
    
    if transactionId != -1:
        try:
            pullFromOSM(url, auth, transactionId)
        except Exception:
            endTransaction(url, auth, True, transactionId)
    
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
