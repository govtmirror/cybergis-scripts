from base64 import b64encode
from optparse import make_option
import json
import urllib
import urllib2
import argparse
import time
import os
import subprocess

def make_request(url, params, auth=None, data=None):
    """
    Prepares a request from a url, params, and optionally authentication.
    """
    req = urllib2.Request(url + urllib.urlencode(params), data=data)

    if auth:
        req.add_header('AUTHORIZATION', 'Basic ' + auth)
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

def getRepoID(geoserver, auth, workspace, datastore):
    params = {}
    url = geoserver+"rest/workspaces/"+workspace+"/datastores/"+datastore+".json"
    request = make_request(url=url, params=params, auth=auth)

    if request.getcode() != 200:
        raise Exception("Get Task Status Failed: Status Code {0}".format(request.getcode()))

    response = json.loads(request.read())
    repoID = None
    for entry in response['dataStore']['connectionParameters']['entry']:
        if entry['@key'] == 'geogig_repository':
            repoID = entry['$']
            break

    return repoID;

def createRepo(path):
    if not os.path.exists(path):
        os.makedirs(path)
    subprocess.Popen("geogig init", cwd=path, shell=True)
    time.sleep(5)

def buildPOSTDataDataStore(name, path):
    file_data ="/opt/cybergis-scripts.git/templates/post_geogig_datastore.xml"
    data = None
    with open (file_data, "r") as f:
        data = f.read().replace('{{name}}', name).replace('{{path}}',path)
    return data
    
def buildPOSTDataLayer(name,nativeName,title):
    file_data ="/opt/cybergis-scripts.git/templates/post_geogig_layer.xml"
    data = None
    with open (file_data, "r") as f:
        data = f.read().replace('{{name}}', name).replace('{{nativeName}}', nativeName).replace('{{title}}', title)
    return data

def createDataStore(verbose, geoserver, workspace, auth, name, path):
    if verbose > 0:
        print('Creating GeoServer Datastore.')
    params = {}
    data = buildPOSTDataDataStore(name, path)
    url = geoserver+"rest/workspaces/"+workspace+"/datastores.json"
    request = make_request(url=url+'?', params=params, auth=auth, data=data)

    if request.getcode() != 201:
        raise Exception("Create data store failed: Status Code {0}".format(request.getcode()))

    #print request.read()
    #response = json.loads(request.read())
    #print response

    #if not response['response']['success']:
    #    raise Exception("An error occurred when creating data store: {0}".format(response['response']['error']))

    if verbose > 0:
        print('Datastore created.')

    #return transactionId;

def createLayer(verbose, geoserver, workspace, auth, datastore, layer, prefix):
    if verbose > 0:
        print('Creating GeoServer Layer for '+layer+".")
    params = {}
    if prefix:
        name = prefix+"_"+layer
    else:
        name = layer
    data = buildPOSTDataLayer(name,layer,name)
    url = geoserver+"rest/workspaces/"+workspace+"/datastores/"+datastore+"/featuretypes.xml"
    
    try:
        request = make_request(url=url+'?', params=params, auth=auth, data=data)
    except:
        raise Exception("Create layer failed: Status Code {0}".format(request.getcode()))

    if request.getcode() != 201:
        raise Exception("Create layer failed: Status Code {0}".format(request.getcode()))
        
    if verbose > 0:
        print('Layer created.')

def getTrees(verbose, url, auth):
    
    params = {'output_format': 'JSON', 'verbose': 'true'}
    request = make_request(url=url+'ls-tree.json?', params=params, auth=auth)

    if request.getcode() != 200:
        raise Exception("Checkout for branch "+branch+" failed: Status Code {0}".format(request.getcode()))
        
    response = json.loads(request.read())
    
    if response['response']['success']:
        try:
          trees = response['response']['node']
          return trees
        except:
          print "ls-tree reported success, but did not have any trees.  No data in OSM?"
          print response
          return None
    else:
        print "----"
        print "List trees failed."
        print "Error Message: "+response['response']['error']
        return None

class Extract(object):

    def __init__(self):
        self.name = None
        self.datastore = None
        self.path = None

def getIndex(element,array):
    try:
        return array.index(element)
    except:
        return -1

def parse_extracts(extracts_file, geoserver, auth, workspace, datastore):
    if extracts_file:
        extracts_string = None
        with open (extracts_file, "r") as f:
            extracts_string = f.read()
        if extracts_string:
            extracts_rows = extracts_string.split("\n")
            header = extracts_rows[0].strip().split("\t")
            iName = getIndex("name",header)
            iDataStore = getIndex("datastore",header)
            iPath = getIndex("path",header)
            extracts_list = []
            for i in range(1,len(extracts_rows)):
                sRow = extracts_rows[i]
                if not sRow:
                    continue

                row = sRow.split("\t")
                extract = Extract()

                if iDataStore >= 0:
                    extract.datastore = row[iDataStore]

                if iName >= 0:
                    extract.name = row[iName]

                if iPath >= 0:
                    extract.path = row[iPath]

                extracts_list.append(extract)

            return extracts_list
        else:
            print "The extracts file is empty."
            return None
    else:
        print "No extracts file specified."
        return None

def processRepo(path,datastore,geoserver,workspace,auth,publish_datastore,publish_layers,verbose):
    #Initialize GeoGig Repository
    if path:
        createRepo(path)

    #Create GeoGig Data store in GeoServer
    if publish_datastore > 0 and geoserver and workspace and datastore and path:
        createDataStore(verbose,geoserver,workspace,auth,datastore,path)

    #Publish GeoGig Trees as Layers
    if publish_layers > 0:
        repo = getRepoID(geoserver, auth, workspace, datastore)
        url_repo = geoserver+'geogig/'+repo+'/'
        trees = getTrees(verbose, url_repo, auth)
        if trees:

            if nodes and ways:
                trees = ([t['path'] for t in trees])
            elif (not nodes) and ways:
                trees = ([t['path'] for t in trees if (not t['path'] in ['node'])])
            elif nodes and (not ways):
                trees = ([t['path'] for t in trees if (not t['path'] in ['way'])])
            else:
                trees = ([t['path'] for t in trees if (not t['path'] in ['node','way'])])

            for tree in trees:
                try:
                    createLayer(verbose, geoserver, workspace, auth, datastore, tree, datastore)
                except:
                    print "Couldn't create layer from datastore "+datastore+" for tree "+tree+"."


def run(args):
    #print args
    #==#
    verbose = args.verbose
    #==#
    publish_datastore = args.publish_datastore
    publish_layers = args.publish_layers
    #==#
    name = args.name
    datastore = args.datastore
    geoserver = parse_url(args.geoserver)
    parent = args.parent
    path = args.path
    workspace = args.workspace
    #==#
    extracts_file = args.extracts
    #==#
    nodes = args.nodes == 1 # Include Nodes?
    ways = args.ways == 1 # Include Ways?
    #url_repo = geoserver+'geogig/'+repo+'/'
    #==#
    auth = None
    if args.username and args.password:
      auth = b64encode('{0}:{1}'.format(args.username, args.password))
    #==#
    print "=================================="
    print "#==#"
    print "CyberGIS Script / geogig_init_repo.py"
    print "Initialize GeoGig repository and optionally add to GeoServer instance."
    print "#==#"
    #==#
    if extracts_file:
        extracts = parse_extracts(extracts_file, geoserver, auth, workspace, datastore)
        if extracts:
            for extract in extracts:
                if extract.path:
                    processRepo(extract.path,extract.datastore,geoserver,workspace,auth,publish_datastore,publish_layers,verbose)
                elif extract.name and parent:
                    if parent.endswith(os.sep):
                        parent = parent[:-1]
                    processRepo(parent+os.sep+extract.name,extract.datastore,geoserver,workspace,auth,publish_datastore,publish_layers,verbose)
        else:
            print "Extracts file was not parsed correctly."
            return 1
    else:
        if path:
            processRepo(path,datastore,geoserver,workspace,auth,publish_datastore,publish_layers,verbose)
        elif name and parent:
            processRepo(parent+os.sep+name,datastore,geoserver,workspace,auth,publish_datastore,publish_layers,verbose)
        else:
            print "Need either path or name and parent"
            return 1
    print "=================================="
