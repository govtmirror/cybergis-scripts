#!/usr/bin/python2.7
import sys
import os
import threading
import time
import Queue
import struct
import numpy
import struct
import gdal
import osr
import gdalnumeric
from gdalconst import *

class RenderThread(threading.Thread):
    def __init__(self, threadID, threadName, queue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
        self.queue = queue
        
    def run(self):
    	process(self.name,self.queue)

def process(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            inBand, outband, y0, y, r, t = q.get()
            queueLock.release()
            #==#
            if t==1:
            	print "Rendering rows "+str(y*r)+" to "+str((y*r)+r)+"."
            	outBand.WriteArray(inBand.ReadAsArray(0,y*r,inBand.XSize,r,inBand.XSize,r),0,y*r)
            elif t==2:
            	print "Rendering row "+str(y0+y)+"."
            	outBand.WriteArray(inBand.ReadAsArray(0,y0+y,inBand.XSize,1,inBand.XSize,1),0,y0+y)
            	
        else:
            queueLock.release()
        #==#
        time.sleep(1)

def main():
	if(len(sys.argv)==8):
		inputFile = sys.argv[1]
		inputBands = int(sys.argv[2])
		alphaFile = sys.argv[3]
		alphaIndex = int(sys.argv[4])
		outputFile = sys.argv[5]
		rows = int(sys.argv[6])
		threads = int(sys.argv[7])
		if threads > 0:
			if(os.path.exists(inputFile) and os.path.exists(alphaFile)):
				if(not os.path.exists(outputFile)):
					inputDataset = gdal.Open(inputFile,GA_ReadOnly)
					alphaDataset = gdal.Open(alphaFile,GA_ReadOnly)
					if ((not inputDataset is None) and (not alphaDataset is None)):
						outputFormat = "GTiff"
						numberOfBands = inputBands+1
						w = inputDataset.RasterXSize
						h = inputDataset.RasterYSize
						r = rows
						outputDataset = initDataset(outputFile,outputFormat,w,h,numberOfBands)
						outputDataset.SetGeoTransform(list(inputDataset.GetGeoTransform()))
						outputDataset.SetProjection(inputDataset.GetProjection())
					
						if threads == 1:
							for b in range(inputBands):
								inBand = inputDataset.GetRasterBand(b+1)
								outBand = outputDataset.GetRasterBand(b+1)
						
								for y in range(int(inBand.YSize/r)):
									outBand.WriteArray(inBand.ReadAsArray(0,y*r,inBand.XSize,r,inBand.XSize,r),0,y*r)

								y0 = inBand.YSize/r
								for y in range(inBand.YSize%r):
									outBand.WriteArray(inBand.ReadAsArray(0,y0+y,inBand.XSize,1,inBand.XSize,1),0,y0+y)
								
							burn(alphaDataset.GetRasterBand(alphaIndex),outputDataset.GetRasterBand(numberOfBands),r)
					
						elif threads > 1:
							
							exitFlag = 0
							queueLock = threading.Lock()
							workQueue = Queue.Queue(0)
							threads = []
							threadID = 1
							
							for threadID in range(threads):
								thread = RenderThread(threadID, ("Thread "+threadID), workQueue)
    								thread.start()
    								threads.append(thread)
    								threadID += 1
							
							queueLock.acquire()
							#Add RGB Tasks
							for b in range(inputBands):
								print "Processing Band"+str(b)
								inBand = inputDataset.GetRasterBand(b+1)
								outBand = outputDataset.GetRasterBand(b+1)
								y0 = inBand.YSize/r
								for y in range(int(inBand.YSize/r)):
									task = inband, outBand, y0, y, r, 1
									workQueue.put(task)
								for y in range(inBand.YSize%r):
									task = inband, outBand, y0, y, r, 2
									workQueue.put(task)
							#Add Alpha Tasks
							inBand = alphaDataset.GetRasterBand(alphaIndex)
							outBand = outputDataset.GetRasterBand(numberOfBands)
							y0 = inBand.YSize/r
							for y in range(int(inBand.YSize/r)):
								task = inband, outBand, y0, y, r, 1
								workQueue.put(task)
							for y in range(inBand.YSize%r):
								task = inband, outBand, y0, y, r, 2
								workQueue.put(task)
							
							queueLock.release()
							print "Queue is full with "+str(qsize)+" tasks."
							print "Rendering threads will now execute."
							while not workQueue.empty():
								pass
							
							exitFlag = 1 #tell's threads it's time to quit
							
							for t in threads:
								t.join()
								
						inputDataset = None
						outputDataset = None
					else:
						print "Error Opening File"
				else:
					print "Output file already exists"
			else:
				print "Input file does not exist."
		else:
			print "Threads needs to be 1 or higher."
	else:
		print "Usage: cybergis-script-burn-alpha.py <input_file> <input_bands> <alpha_file> <alpha_band_index> <output_file> <rows> <threads>"

def burn(inBand,outBand,rows):
	r = rows
	for y in range(int(inBand.YSize/r)):
		outBand.WriteArray(inBand.ReadAsArray(0,y*r,inBand.XSize,r,inBand.XSize,r),0,y*r)

	y0 = inBand.YSize/r
	for y in range(inBand.YSize%r):
		outBand.WriteArray(inBand.ReadAsArray(0,y0+y,inBand.XSize,1,inBand.XSize,1),0,y0+y)
        
def initDataset(outputFile,f,w,h,b):
    driver = gdal.GetDriverByName(f)
    metadata = driver.GetMetadata()
    return driver.Create(outputFile,w,h,b,gdal.GDT_Byte,['ALPHA=YES'])

main()    
