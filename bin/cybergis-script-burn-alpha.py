#!/usr/bin/python2.7
import sys
import os
import threading
import time
import struct
import numpy
import struct
import gdal
import osr
import gdalnumeric
from gdalconst import *

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
					
						if threads===1:
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
							for b in range(inputBands):
								inBand = inputDataset.GetRasterBand(b+1)
								outBand = outputDataset.GetRasterBand(b+1)
						
								for y in range(int(inBand.YSize/r)):
									outBand.WriteArray(inBand.ReadAsArray(0,y*r,inBand.XSize,r,inBand.XSize,r),0,y*r)

								y0 = inBand.YSize/r
								for y in range(inBand.YSize%r):
									outBand.WriteArray(inBand.ReadAsArray(0,y0+y,inBand.XSize,1,inBand.XSize,1),0,y0+y)
								
							burn(alphaDataset.GetRasterBand(alphaIndex),outputDataset.GetRasterBand(numberOfBands),r)
						
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
	#for y in range(inBand.YSize):
	#	inLine = inBand.ReadAsArray(0,y,inBand.XSize,1,inBand.XSize,1)
	#	outBand.WriteArray(inLine,0,y)
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
