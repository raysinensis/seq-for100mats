import numpy
import csv
import re

##read gene list
plusfile = "/home/rf/Desktop/UTR/plusgenes.txt"
minusfile = "/home/rf/Desktop/UTR/minusgenes.txt"

plusgenes = (open(plusfile, 'r').read()).splitlines()
plusgenes = list(set(plusgenes))
pluscount = len(plusgenes)
plusarray = numpy.asarray(plusgenes)
plusarray = plusarray[..., numpy.newaxis]
appendcol = numpy.zeros((pluscount,2),)
plusarray = numpy.append(plusarray,appendcol, 1)

minusgenes = (open(minusfile, 'r').read()).splitlines()
minusgenes = list(set(minusgenes))
minuscount = len(minusgenes)
minusarray = numpy.asarray(minusgenes)
minusarray = minusarray[..., numpy.newaxis]
appendcol = numpy.zeros((minuscount,2),)
minusarray = numpy.append(minusarray,appendcol, 1)

##load start site from csv file
with open("/home/rf/Desktop/UTR/startcodon.csv", "rb") as csvfile:
        datareader = csv.reader(csvfile)
        count = 0
        for row in datareader:
		if count>=0:
			count+=1
			currenttxt = str(row)
			currentline = currenttxt.split("\\t")
  			genename = re.search('gene_name \"(.+?)\"',currenttxt).group(1)
			startsite = int(currentline[3])
			try:
				filenumber = int(numpy.where(plusarray == genename)[0])
				print(filenumber)
			except Exception, e:
				print(e)
			if plusarray[filenumber,1] == '0.0':
				plusarray[filenumber,1] = startsite
			elif startsite < plusarray[filenumber,1]:
				plusarray[filenumber,1] = startsite

##load stop site
with open("/home/rf/Desktop/UTR/stopcodon.csv", "rb") as csvfile:
        datareader = csv.reader(csvfile)
        count = 0
        for row in datareader:
		if count>=0:
			count+=1
			currenttxt = str(row)
			currentline = currenttxt.split("\\t")
  			genename = re.search('gene_name \"(.+?)\"',currenttxt).group(1)
			stopsite = currentline[4]
			try:
				filenumber = int(numpy.where(plusarray == genename)[0])
				print(filenumber)
				if stopsite > float(plusarray[filenumber,2]):
					plusarray[filenumber,2] = stopsite
			except Exception, e:
				print("not found")

##doing the same for minus strand genes
with open("/home/rf/Desktop/UTR/stopcodon.csv", "rb") as csvfile:
        datareader = csv.reader(csvfile)
        count = 0
        for row in datareader:
		if count>=0:
			count+=1
			currenttxt = str(row)
			currentline = currenttxt.split("\\t")
  			genename = re.search('gene_name \"(.+?)\"',currenttxt).group(1)
			stopsite = int(currentline[3])
			try:
				filenumber = int(numpy.where(minusarray == genename)[0])
				print(stopsite)
				if minusarray[filenumber,2] == '0.0':
					minusarray[filenumber,2] = stopsite
					print(minusarray[filenumber,2])
				elif stopsite < minusarray[filenumber,2]:
					minusarray[filenumber,2] = stopsite
					print("2")
			except Exception, e:
				print("not found")

with open("/home/rf/Desktop/UTR/startcodon.csv", "rb") as csvfile:
        datareader = csv.reader(csvfile)
        count = 0
        for row in datareader:
		if count>=0:
			count+=1
			currenttxt = str(row)
			currentline = currenttxt.split("\\t")
  			genename = re.search('gene_name \"(.+?)\"',currenttxt).group(1)
			startsite = currentline[4]
			try:
				filenumber = int(numpy.where(minusarray == genename)[0])
				print(startsite)
				if startsite > float(minusarray[filenumber,1]):
					minusarray[filenumber,1] = startsite
			except Exception, e:
				print("not found")
