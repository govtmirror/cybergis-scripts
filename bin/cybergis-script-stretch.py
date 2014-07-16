#!/usr/bin/python2.7
import sys
import os
import time
import datetime
from multiprocessing import Process, Lock, Queue, cpu_count
import struct
import numpy
from xml.dom.minidom import parse, parseString
import gdal
import osr
import gdalnumeric
from gdalconst import *

exitFlag = 0
queueLock = None
writeLock = None
workQueue = None
tasks = None

class Tasks(object):
	def __init__(self):
		self.tasks = []
	
	def add(self,task):
		self.tasks.append(task)
	
	def get(self,task):
		return self.tasks[task]
		
class RenderSubprocess(object):
    def __init__(self, processID, processName, queue, tasks):
        self.processID = processID
        self.processName = processName
        self.queue = queue
        self.tasks = tasks
        #Variable#
        self.strip = None
        self.strip_stretched = None
        self.task = None
        self.tries = 3
        
    def run(self):
    	while not exitFlag:
    		if self.strip is None:
    			queueLock.acquire()
        		if not workQueue.empty():
            			b, inBand, outBand, lut, y0, y, r, t = self.task = self.tasks.get(self.queue.get())
            			queueLock.release()
            			#==#
            			if t==1:
			            	#print self.processName+" reading rows "+str(y*r)+" to "+str((y*r)+r-1)+" in band "+str(b)+"."
            				try:
            					self.strip = inBand.ReadAsArray(0,y*r,inBand.XSize,r,inBand.XSize,r)
            					self.tries = 10
            				except:
            					self.strip = None
            					self.strip_stretched = None
            					print "read failed.  will try again later."
            					print "y:"+str(y)
            					print "r:"+str(r)
            				
            			elif t==2:
			            	#print self.processName+" reading row "+str((y0*r)+y)+" in band "+str(b)+"."
            				try:
            					self.strip = inBand.ReadAsArray(0,(y0*r)+y,inBand.XSize,1,inBand.XSize,1)
            					self.tries = 10
            				except:
            					self.strip = None
            					self.strip_stretched = None
            					print "read failed.  will try again later."
            					print "y0:"+str(y0)
            					print "y:"+str(y)
            					print "r:"+str(r)
            					print "(y0*r)+y:"+str((y0*r)+y)
            				
        		else:
            			queueLock.release()
            	elif (not self.strip is None) and (self.strip_stretched is None):
            		b, inBand, outBand, lut, y0, y, r, t = self.task
            		self.strip_stretched = lut[self.strip]
        	elif (not self.strip is None) and (not self.strip_stretched is None):
        		if self.tries > 0:
        			writeLock.acquire()
        			b, inBand, outBand, lut, y0, y, r, t = self.task
        			if t==1:
			            	#print self.processName+" writing rows "+str(y*r)+" to "+str((y*r)+r-1)+" in band "+str(b)+"."
            				try:
	            				outBand.WriteArray(self.strip_stretched,0,y*r)
            					self.strip = None
            					self.strip_stretched = None
            				except:
	            				self.tries = self.tries - 1
            					print "write failed.  "+str(self.tries)+" more tries."
            			elif t==2:
			            	#print self.processName+" writing row "+str((y0*r)+y)+" in band "+str(b)+"."
            				try:
            					outBand.WriteArray(self.strip_stretched,0,(y0*r)+y)
            					self.strip = None
            					self.strip_stretched = None
            				except:
            					self.tries = self.tries -1
            					print "write failed.  "+str(self.tries)+" more tries."
            			writeLock.release()
            		else:
            			print "abandoning write"
            			self.strip = None
            			self.strip_stretched = None
            	else:
            	    print "abandoning task.  This should never happen."
            	    self.strip = None
            	    self.strip_stretched = None
            	    
        	time.sleep(1)

def execute(subprocess):
	subprocess.run()

class BreakPoint:

	def __init__(self, i = None, o = None):
		self.i = i #Should be double; even though it is most frequently an int
		self.o = o

class Line:

	def __init__(self, b0, b1):
		self.x0 = b0.i
		self.y0 = b0.o
		self.x1 = b1.i
		self.y1 = b1.o
		self.n = float(self.y1-self.y0)
		self.d = float(self.x1-self.x0)
		if self.d != 0:
			self.m = self.n/self.d
			self.b = self.y0 - self.m*self.x0
		else:
			self.m = None
			self.b = None

	def min(self):
		return self.x0
	
	def max(self):
		return self.x1

	def contains(self, x):
		return x>=self.x0 and x <=self.x1

	def calc(self, x):
		if self.d != 0:
			return int(round(self.m*x+self.b))
		elif self.d == 0 and self.y1 == self.y0:
			return self.y1
		else:
			return x

class Lines:

	def __init__(self, bps):
		self.lines = []
		for i in range(len(bps)-1):
			if (not (bps[i] is None)) and (not (bps[i+1] is None)):
				self.lines.append(Line(bps[i],bps[i+1]))
	
	def size(self):
		return len(self.lines)	

	def min(self):
		return self.lines[0].min()
	
	def max(self):
		return self.lines[len(self.lines)-1].max()

	def calc(self, x):
		y = x
		for line in self.lines:
			if line.contains(x):
				y = line.calc(x)
				break
		return y

class LookUpTable:
	
	def __init__(self,bps):
		self.lines = Lines(bps)
		self.table = []
		self.min = int(self.lines.min())
		self.max = int(self.lines.max())
		
		for i in range(0,256):
			self.table.append(self.lines.calc(i))
		
class LookUpTable2:

	def __init__(self,bps_red,bps_green,bps_blue):
		self.lines_red = Lines(bps_red)
		self.lines_green = Lines(bps_green)
		self.lines_blue = Lines(bps_blue)
		self.table = []
		for i in range(0,256):
			self.table.append(int((self.lines_red.calc(i)+self.lines_green.calc(i)+self.lines_blue.calc(i))/3.0))

class LookUpTables:

	def __init__ (self, filename):
		self.bps_red = None
		self.bps_green = None
		self.bps_blue = None
		self.tables = None
		self.table = None

		self.file = None
		self.valid = True

		self.init_breakpoints(filename)
		self.init_tables()

	def init_breakpoints(self,filename):
                self.bps_red = []
                self.bps_green = []
                self.bps_blue = []

		if filename.endswith(".cbp") or filename.endswith(".txt"):
			lines = None
			file = open(filename,"r")
			with open(filename) as f:
				lines = f.readlines()
			
			band = -1
			for line in lines:
				line = line.strip()
				if line=="":
					continue
				elif line=="rgbversion8.3":
					continue
				elif line.startswith("#"):
					continue
				elif line=="RGB":
					band = band+1
				elif line.startswith("Band"):
					band = int(line.split()[1].strip(' \t\n\r'))-1
				elif line.startswith("Break") or line.startswith("-"):
					if band==0:
						self.bps_red.append(None)
					elif band==1:
						self.bps_green.append(None)
					elif band==2:
						self.bps_blue.append(None)
				else:
					terms = line.split()
					bp = BreakPoint(float(terms[0].strip(' \t\n\r')),float(terms[1].strip(' \t\n\r')))
					if band==0:
						self.bps_red.append(bp)
					elif band==1:
						self.bps_green.append(bp)
					elif band==2:
						self.bps_blue.append(bp)

		elif filename.endswith(".qml"):
			file = open(filename,"r")
			dom = parse(file)
			minRed = -1
			maxRed = -1
			minGreen = -1
			maxGreen = -1
			minBlue = -1
			maxBlue = -1
			for nRasterRenderer in dom.getElementsByTagName("rasterrenderer"):
				for node in nRasterRenderer.childNodes:
					#print node.toxml()
					if node.nodeType != node.TEXT_NODE:
						if node.tagName=="redContrastEnhancement":
							minRed = float(node.getElementsByTagName("minValue")[0].firstChild.nodeValue)
							maxRed = float(node.getElementsByTagName("maxValue")[0].firstChild.nodeValue)
						elif node.tagName=="greenContrastEnhancement":
							minGreen = float(node.getElementsByTagName("minValue")[0].firstChild.nodeValue)
							maxGreen = float(node.getElementsByTagName("maxValue")[0].firstChild.nodeValue)
						elif node.tagName=="blueContrastEnhancement":
							minBlue = float(node.getElementsByTagName("minValue")[0].firstChild.nodeValue)
							maxBlue = float(node.getElementsByTagName("maxValue")[0].firstChild.nodeValue)
			if minRed!=-1 and maxRed!=-1:
				self.bps_red.extend(self.buildBreakPoints(minRed,maxRed))
			if minGreen!=-1 and maxGreen!=-1:
				self.bps_green.extend(self.buildBreakPoints(minGreen,maxGreen))
                        if minBlue!=-1 and maxBlue!=-1:
				self.bps_blue.extend(self.buildBreakPoints(minBlue,maxBlue))
			

	def buildBreakPoints(self,minValue,maxValue):
		bps = []
		bps.append(BreakPoint(0.0,0.0))
		bps.append(BreakPoint(minValue,0.0))
		bps.append(BreakPoint(maxValue,255.0))
		bps.append(BreakPoint(255.0,255.0))
		return bps
	
	def init_tables(self):
		self.tables = []
		self.tables.append(LookUpTable(self.bps_red))
		self.tables.append(LookUpTable(self.bps_green))
		self.tables.append(LookUpTable(self.bps_blue))
		self.tables.append(LookUpTable2(self.bps_red,self.bps_green,self.bps_blue))

	def isValid(self):
		return self.valid;

def main():
	start=datetime.now()
	if(len(sys.argv)==6):
		inputFile = sys.argv[1]
		breakPointsFile = sys.argv[2]
		outputFile = sys.argv[3]
		rows = int(sys.argv[4])
		numberOfThreads = int(sys.argv[5])
		if numberOfThreads > 0:
			if(os.path.exists(inputFile) and os.path.exists(breakPointsFile)):
				if(not os.path.exists(outputFile)):
					inputDataset = gdal.Open(inputFile,GA_ReadOnly)
					lookUpTables = LookUpTables(breakPointsFile)
					if ((not inputDataset is None) and (lookUpTables.isValid())):
						outputFormat = "HFA"
						numberOfBands = 3
						w = inputDataset.RasterXSize
						h = inputDataset.RasterYSize
						outputDataset = initDataset(outputFile,outputFormat,w,h,numberOfBands)
						outputDataset.SetGeoTransform(list(inputDataset.GetGeoTransform()))
						outputDataset.SetProjection(inputDataset.GetProjection())
						
						if numberOfThreads == 1:
							for b in range(numberOfBands):
								print "Stretching Band "+str(b+1)
								lut = numpy.array(lookUpTables.tables[b].table)
								inBand = inputDataset.GetRasterBand(b+1)
								outBand = outputDataset.GetRasterBand(b+1)
						
								r = rows
								for y in range(int(inBand.YSize/r)):
									outBand.WriteArray(lut[inBand.ReadAsArray(0,y*r,inBand.XSize,r,inBand.XSize,r)],0,y*r)
						
								y0 = inBand.YSize/rows
								for y in range(inBand.YSize%r):
									outBand.WriteArray(lut[inBand.ReadAsArray(0,y0+y,inBand.XSize,1,inBand.XSize,1)],0,y0+y)
						elif numberOfThreads > 1:
                            print "not fully implemented yet"
                            global exitFlag
                            global queueLock
                            global writeLock
                            global workQueue
                            global tasks
							#
                            exitFlag = 0
                            queueLock = Lock()
                            writeLock = Lock()
                            workQueue = Queue(0)
                            tasks = Tasks()
							#
							for b in range(inputBands):
								print "Adding tasks for band "+str(b+1)
								lut = numpy.array(lookUpTables.tables[b].table)
								inBand = inputDataset.GetRasterBand(b+1)
								outBand = outputDataset.GetRasterBand(b+1)
								y0 = int(inBand.YSize/r)
								for y in range(int(inBand.YSize/r)):
									task = b+1, inBand, outBand, lut, y0, y, r, 1
									tasks.add(task)
								for y in range(inBand.YSize%r):
									task = b+1, inBand, outBand, lut, y0, y, r, 2
									tasks.add(task)
									
							print "tasks in main queue: "+str(len(tasks.tasks))
							#Add tasks to queue
							queueLock.acquire()
							for taskID in range(len(tasks.tasks)):
								workQueue.put(taskID)
							queueLock.release()
							
							processes = initProcesses(numberOfThreads)

							print "Queue is full with "+str(workQueue.qsize())+" tasks."
							print "Rendering threads will now execute."
							while not workQueue.empty():
								pass
							
							exitFlag = 1 #tell's threads it's time to quit
							
							for process in processes:
								process.join()
					
						inputDataset = None
						outputDataset = None
						print datetime.now()-start
					else:
						print "Error Opening File"
				else:
					print "Output file already exists"
			else:
				print "Input file does not exist."
		else:
			print "You need at least 1 thread."
	else:
		print "Usage: cybergis-script-stretch.py <input_file> <breakpoints_file> <output_file> <rows> <threads>"

def initDataset(outputFile,f,w,h,b):
    driver = gdal.GetDriverByName(f)
    metadata = driver.GetMetadata()
    return driver.Create(outputFile,w,h,b,gdal.GDT_Byte,['ALPHA=YES'])

def initProcesses(count)
    print str(cpu_count())+" CPUs are available."
    processes = []
    processID = 1
    for processID in range(count):
        subprocess = RenderSubprocess(processID, ("Thread "+str(processID)), workQueue, tasks)
        process = Process(target=execute,args=(subprocess,))
        process.start()
        processes.append(process)
        processID += 1
    print "Initialized "+str(count)+" threads."
    return processes

main()
