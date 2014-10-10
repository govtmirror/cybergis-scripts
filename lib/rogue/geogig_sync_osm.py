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

    print('Transaction started.')
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

    print('Transaction ended.')

def checkout(url, auth, branch, transactionId):
    print "Checking out "+branch+" branch..."
    params = {'output_format': 'JSON', 'branch': branch, 'transactionId':transactionId}
    request = make_request(url=url+'checkout.json?', params=params, auth=auth)

    if request.getcode() != 200:
        raise Exception("Checkout for branch "+branch+" failed: Status Code {0}".format(request.getcode()))
        
    response = json.loads(request.read())
    
    #taskID = response['task']['id']
    #print response

    newBranch = response['response']['NewTarget']
    print "Checked out "+newBranch+' branch.'
    return newBranch

def getTaskStatus(url, auth, taskID, printStatus):
    #print('Downloading from OpenStreetMap ...')
    params = {}
    request = make_request(url=url+'/'+str(taskID)+'.json', params=params, auth=auth)

    #print request.getcode()
    if request.getcode() != 200:
        raise Exception("Get Task Status Failed: Status Code {0}".format(request.getcode()))
    
    response = json.loads(request.read())

    taskStatus = response['task']['status']
    
    if printStatus:
        if taskStatus == "RUNNING":
            #print response
            #taskAmount = response['task']['amount']
            taskAmount = "#" #Amount value isn't showing up in response.
            print "++Task "+str(taskID)+" is running and "+taskAmount+" percentage complete."
        elif taskStatus == "FAILED":
            errorMessage = response['task']['error']['message']
            print "++Task "+str(taskID)+" failed with error message: "+errorMessage+"."
        elif taskStatus == "FINISHED":
            print response
            print "++Task "+str(taskID)+" is finished."
        else:
            print "++Task "+str(taskID)+" is "+taskStatus+"."
    
    return taskStatus;
    
def cancelTask(url, auth, taskID, printStatus):
    print('Downloading from OpenStreetMap ...')
    params = {}
    request = make_request(url=url+'/'+str(taskID)+'.json?cancel=true', params=params, auth=auth)

    if request.getcode() != 200:
        raise Exception("Could not cancel task: Status Code {0}".format(request.getcode()))
    
    response = json.loads(request.read())

    taskStatus = response['task']['status']
    
    if printStatus:
        if taskStatus == "CANCELLED":
            print "++Task "+str(taskID)+" was cancelled."
        else:
            print "++Error.  Could not cancel task "+str(taskID)+"."
    
    return taskStatus;

def waitOnTask(url, auth, taskID):
    maxTime = 30
    timeSlept = 0
    sleepCycle = 5
    taskStatus = None
    print "----------------------------------"
    print "Waiting for task "+str(taskID)+"..."
    print "Maximum wait time is "+str(maxTime)+" seconds."
    while timeSlept < maxTime:
        taskStatus = getTaskStatus(url, auth, taskID, True)
        if not (taskStatus in ['WAITING','RUNNING']):
            break
        #print "Time Slept: "+str(timeSlept)
        time.sleep(sleepCycle)
        timeSlept += sleepCycle
    
    if taskStatus in ['WAITING','RUNNING']:
        print "Task "+str(taskID)+" timed out after "+str(timeSlept)+" seconds."
        print "Attempting to cancel task "+str(taskID)
        maxTime = 30
        timeSlept = 0
        sleepCycle = 1
        while timeSlept < maxTime:
            taskStatus = cancelTask(url, auth, taskID, True)
            if not (taskStatus in ['WAITING','RUNNING']):
                break
            time.sleep(sleepCycle)
            timeSlept += sleepCycle
    
    print "Task "+str(taskID)+" is done"

def downloadFromOSM(url, auth, transactionId, update, mapping, bbox):
    print('Downloading from OpenStreetMap ...')
    params = {'output_format': 'JSON', 'update': update, 'mapping': mapping, 'bbox': bbox, 'transactionId':transactionId}
    request = make_request(url=url+'osm/download.json?', params=params, auth=auth)

    if request.getcode() != 200:
        raise Exception("OSM Download failed: Status Code {0}".format(request.getcode()))
        
    response = json.loads(request.read())
    
    taskID = response['task']['id']
    
    #print response
    if response['task']['status'] == 'FAILED':
        raise Exception("An error occurred when pulling new data from OSM: {0}".format(response['task']['status']))

    if response['task']['status'] == 'WAITING':
        print('Download from OpenStreetMap is waiting to be processed.  Task ID is '+str(taskID)+'.')
    
    if response['task']['status'] == 'RUNNING':
        print('Download from OpenStreetMap is being processed.  Task ID is '+str(taskID)+'.')
        
    return taskID;
 
def parse_url(url):
    
    if (url is None) or len(url) == 0:
        return None
    
    index = url.rfind('/')

    if index != (len(url)-1):
        url += '/'
    
    return url

def parse_bbox(extent):
    file_extent ="/opt/cybergis-osm-mappings.git/extents/"+extent+".txt"
    bbox = None
    with open (file_extent, "r") as f:
        bbox = f.read().replace('\n', '')
    return bbox

def run(args):
    #==#
    geoserver = parse_url(args.geoserver)
    repo = args.repo
    url_repo = geoserver+'geogig/'+repo+'/'
    url_tasks = geoserver+'geogig/tasks'
    #==#
    authorname = args.authorname
    authoremail = args.authoremail
    #==#
    auth = None
    if args.username and args.password:
      auth = b64encode('{0}:{1}'.format(args.username, args.password))
    #==#
    update = args.update in ["1","y","t","true"]
    bbox = parse_bbox(args.extent)
    mapping = args.mapping
    print "=================================="
    print "#==#"
    print "CyberGIS Script / geogig_sync_osm.py"
    print "Downloading Updates from OpenStreetMap"
    print "#==#"

    boolean valid:   
    if update:
        pass
    elif bbox and mapping:
       pass
    else:
        return "Update is false and no new data will be brought in because the extent and mapping aren't specified"

    transID = -1
    try:
        transID = beginTransaction(url_repo, auth)
    except Exception:
        transID = -1
        raise
    
    if transID != -1:
        taskID = -1
        #==#
        #Checkout master branch.  See: https://github.com/boundlessgeo/GeoGig/issues/788
        try:
            checkout(url_repo, auth, 'master', transID)
            taskID = downloadFromOSM(url_repo, auth, transID, update, mapping, bbox)
        except Exception:
            taskID = -1
            endTransaction(url_repo, auth, True, transID)
            raise
        
        if taskID != -1:
            waitOnTask(url_tasks, auth, taskID)
  
        #==#
        #Checkout master branch.  See: https://github.com/boundlessgeo/GeoGig/issues/788
        try:
            checkout(url_repo, auth, 'master', transID)
        except Exception:
            pass
 
    try:
        endTransaction(url_repo, auth, False, transID)
    except Exception:
        pass
    
    print "=================================="

parser = argparse.ArgumentParser(description='Synchronize GeoGig repository with OpenStreetMap (OSM)')

parser.add_argument("repo", help="The GeoServer id of the GeoGig repository you want to sync.")
parser.add_argument("update", help="true/false.  Update existing features only or download new features.  If false, extent and mapping are required.")

parser.add_argument("--geoserver", help="The url of the GeoServer servicing the GeoGig repository.")
parser.add_argument("--username", help="The username to use for basic auth requests.")
parser.add_argument("--password", help="The password to use for basic auth requests.")
parser.add_argument("--authorname", help="The author name to use when merging non-conflicting branches.")
parser.add_argument("--authoremail", help="The author email to use when merging non-conflicting branches.")
parser.add_argument("--extent", help="The extent of the OpenStreetMap extract. For example, basic:buildings_and_roads.")
parser.add_argument("--mapping", help="The mapping of the OpenStreetMap extract.  For example, dominican_republic:santo_domingo.")
  
args = parser.parse_args()
run(args)
