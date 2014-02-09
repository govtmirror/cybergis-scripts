#!/usr/bin/python2.7
import sys
import os
import struct
import numpy
from xml.dom.minidom import parse, parseString

def main():
	if(len(sys.argv)==3):
		configFile = sys.argv[1]
		deploymentDirectory = sys.argv[2]
		if os.path.exists(inputFile) :
			if not os.path.exists(deploymentDirectory):
				print "test"
			else:
				print "Deployment directory already exists"
		else:
			print "Config file does not exist."
	else:
		print "Usage: cybergis-script-client-deploy.py <config_file> <deployment_directory>"

main()
