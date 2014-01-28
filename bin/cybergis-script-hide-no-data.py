import sys
import os
import struct
import numpy
import struct
import gdal
import osr
import gdalnumeric
from gdalconst import *

def main():
	
	if(len(sys.argv)==3):
		inputFile = sys.argv[1]
		outputFile = sys.argv[2]
		if(os.path.exists(inputFile)):
			if(not os.path.exists(outputFile)):
				inputDataset = gdal.Open(inputFile,GA_ReadOnly)
				if not (inputDataset is None):
					outputFormat = "GTiff"
					numberOfBands = 4
					w = inputDataset.RasterXSize
					h = inputDataset.RasterYSize

					outputDataset = initDataset(outputFile,outputFormat,w,h,numberOfBands)
					outputDataset.SetGeoTransform(list(inputDataset.GetGeoTransform()))
					outputDataset.SetProjection(inputDataset.GetProjection())

					outputDataset.GetRasterBand(1).WriteArray(inputDataset.GetRasterBand(1).ReadAsArray())
					outputDataset.GetRasterBand(2).WriteArray(inputDataset.GetRasterBand(2).ReadAsArray())
					outputDataset.GetRasterBand(3).WriteArray(inputDataset.GetRasterBand(3).ReadAsArray())
					hideNoData(inputDataset.GetRasterBand(1),outputDataset.GetRasterBand(4))
				inputDataset = None
				outputDataset = None
				else:
					print "Error Opening File"
			else:
					print "Output file already exists"
		else:
			print "Input file does not exist."
	else:
		print "Usage: cybergis-script-hide-no-data.py <input_file> <output_file>"

def hideNoData(inBand,outBand):
	noData = inBand.GetNoDataValue()
	for y in range(inBand.YSize):
		inLine = inBand.ReadAsArray(0,y,inBand.XSize,1,inBand.XSize,1)
		outLine = numpy.choose(numpy.equal(inLine,noData),(inLine,0))
		outLine = numpy.choose(numpy.not_equal(inLine,noData),(outLine,0xFF))
		outBand.WriteArray(outLine,0,y)

def printGeneralInformation(dataset):
	print 'Driver: ', dataset.GetDriver().ShortName,'/',dataset.GetDriver().LongName
	print 'Size is ',dataset.RasterXSize,'x',dataset.RasterYSize,'x',dataset.RasterCount
	print 'Projection is ',dataset.GetProjection()
	geotransform = dataset.GetGeoTransform()
	if not geotransform is None:
		print 'Origin = (',geotransform[0], ',',geotransform[3],')'
		print 'Pixel Size = (',geotransform[1], ',',geotransform[5],')'
	for i in range(dataset.RasterCount):
		printBandInformation(dataset.GetRasterBand(i+1))

def printBandInformation(band):
	print 'Band Type=',gdal.GetDataTypeName(band.DataType)
	min = band.GetMinimum()
	max = band.GetMaximum()
	if min is None or max is None:
		(min,max) = band.ComputeRasterMinMax(1)
	print 'Min=%.3f, Max=%.3f' % (min,max)

	if band.GetOverviewCount() > 0:
		print 'Band has ', band.GetOverviewCount(), ' overviews.'

	if not band.GetRasterColorTable() is None:
		print 'Band has a color table with ',band.GetRasterColorTable().GetCount(), ' entries.'

def initDataset(outputFile,f,w,h,b):
	driver = gdal.GetDriverByName(f)
	metadata = driver.GetMetadata()
	return driver.Create(outputFile,w,h,b,gdal.GDT_Byte)

#Start Process
main()
