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

def run(args):
    #print args
    #==#
    verbose = args.verbose
    #==#
    publish_datastore = args.publish_datastore
    publish_layers = args.publish_layers
    #==#
    name = args.name
    datastore = name
    geoserver = parse_url(args.geoserver)
    path = args.path
    workspace = args.workspace
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
    #Initialize GeoGig Repository
    if path:
        createRepo(path)
    
    #Create GeoGig Data store in GeoServer
    if publish_datastore > 0 and args.geoserver and args.workspace and args.name and args.path:
        createDataStore(verbose,geoserver,workspace,auth,name,path)

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
                    
    print "=================================="
