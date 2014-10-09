from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse
import time

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

def getTaskStatus(url, auth, taskID):
    print('Downloading from OpenStreetMap ...')
    params = {'output_format': 'JSON', 'update': 'true'}
    request = make_request(url=url+'/'+str(taskID)+'+?', params=params, auth=auth)

    if request.getcode() != 200:
        raise Exception("Get Task Status Failed: Status Code {0}".format(request.getcode()))
        
    response = json.loads(request.read())

    taskStatus = response['task']['status']
    
    print taskStatus
    return taskID;

def waitOnTask(url, auth, taskID):
    print "Waiting for task "+str(taskID)+"..."
    
    maxTime = 20
    timeSlept = 0
    sleepCycle = 2
    
    while timeSlept < maxTime and getTaskStatus(url, auth,taskID) in ['WAITING','RUNNING']:
        time.sleep(sleepCycle)
        timeSlept += sleepCycle
        
    print "Task "+str(taskID)+" is done"

def downloadFromOSM(url, auth, transactionId):
    print('Downloading from OpenStreetMap ...')
    params = {'output_format': 'JSON', 'update': 'true'}
    request = make_request(url=url+'osm/download.json?', params=params, auth=auth)

    if request.getcode() != 200:
        raise Exception("OSM Download failed: Status Code {0}".format(request.getcode()))
        
    response = json.loads(request.read())

    print response
    if response['task']['status'] == 'FAILED':
        raise Exception("An error occurred when pulling new data from OSM: {0}".format(response['task']['status']))

    print('Download from OpenStreetMap complete.')
    
    taskID = response['task']['id']
        
    return taskID;
 
def parse_geoserver(url):
    
    if (url is None) or len(url) == 0:
        return None
    
    index = url.rfind('/')

    if index != (len(url)-1):
        url += '/'
    
    return url

def run(args):
    #url = parse_url(args)
    #if url is None:
    #    print "Please specify a url"
    #    return 1
    
    geoserver = parse_url(args.geoserver)
    repo = args.repo
    url_repo = geoserver+'geogig/'+repo+'/'
    url_tasks = geoserver+'geogig/tasks'
    
    authorname = args.authorname
    authoremail = args.authoremail
    auth = None
    if args.username and args.password:
      auth = b64encode('{0}:{1}'.format(args.username, args.password))

    transID = -1
    try:
        transID = beginTransaction(url_repo, auth)
    except Exception:
        transID = -1
        raise
    
    if transID != -1:
        taskID = -1
        try:
            taskID = downloadFromOSM(url_repo, auth, transID)
        except Exception:
            taskID = -1
            endTransaction(url_repo, auth, True, transID)
            raise
        
        if taskID != -1:
            waitOnTask(url_tasks, auth, taskID)
    
    try:
        endTransaction(url_repo, auth, False, transID)
    except Exception:
        pass

parser = argparse.ArgumentParser(description='Synchronize GeoGig repository with OpenStreetMap (OSM)')
parser.add_argument("--geoserver", help="The url of the GeoServer servicing the GeoGig repository.")
parser.add_argument("--repo", help="The GeoServer id of the GeoGig repository you want to sync.")
parser.add_argument("--username", help="The username to use for basic auth requests.")
parser.add_argument("--password", help="The password to use for basic auth requests.")
parser.add_argument("--authorname", help="The author name to use when merging non-conflicting branches.")
parser.add_argument("--authoremail", help="The author email to use when merging non-conflicting branches.")
  
args = parser.parse_args()
run(args)
