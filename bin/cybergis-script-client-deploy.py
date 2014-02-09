#!/usr/bin/python2.7
import sys
import os
import shutil
import zipfile
import struct
import numpy
import urllib
import urllib2
from xml.dom.minidom import parse, parseString


URL_TEMPLATES = "https://github.com/state-hiu/cybergis-client-templates/archive/master.zip"

NAME_TEMPLATE = "osm"

def main():
	if(len(sys.argv)==3):
		configFile = sys.argv[1]
		deploymentDirectory = sys.argv[2]
		print "configFile: "+configFile
		print "deploymentDirectory: "+deploymentDirectory
		if os.path.exists(configFile) :
			if not os.path.exists(deploymentDirectory):
				os.makedirs(deploymentDirectory)
				os.makedirs(deploymentDirectory+os.sep+".cybergis")
				shutil.copyfile(configFile,deploymentDirectory+os.sep+".cybergis"+os.sep+os.path.basename(configFile))
				zipPath = deploymentDirectory+os.sep+".cybergis"+os.sep+"templates"+os.sep+"templates.zip"
				print zipPath
				os.makedirs(deploymentDirectory+os.sep+".cybergis"+os.sep+"templates")
				urllib.urlretrieve(URL_TEMPLATES,zipPath)
				with zipfile.ZipFile(zipPath) as zipFile:
					#print zipFile.namelist()
					for name in z.namelist():
						if name.startswith("cybergis-client-templates-master/1.0/"+NAME_TEMPLATE+"/")
							if f.endswith('/'):
								os.mkdir(deploymentDirectory+os.sep+NAME_TEMPLATE)
							zipFile.extract("cybergis-client-templates-master/1.0/osm/",deploymentDirectory)
			else:
				print "Deployment directory already exists"
		else:
			print "Config file does not exist."
	else:
		print "Usage: cybergis-script-client-deploy.py <config_file> <deployment_directory>"

main()
