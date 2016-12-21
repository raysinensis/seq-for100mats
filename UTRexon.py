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

##load stop site from csv file
with open("/home/rf/Desktop/UTR/stopcodon.csv", "rb") as csvfile:
        datareader = csv.reader(csvfile)
        count = 0
        for row in datareader:
		if count>=0:
			count+=1
			currenttxt = str(row)
			currentline = currenttxt.split("\\t")
  			genename = re.search('gene_name \"(.+?)\"',currenttxt).group(1)
			stopsite = float(currentline[3])
			try:
				filenumber = int(numpy.where(plusarray == genename)[0])
				print(filenumber)
			except Exception, e:
				print(e)
				continue
			if plusarray[filenumber,2] == '0.0':
				plusarray[filenumber,2] = stopsite
				print("initial match")
			elif stopsite < float(plusarray[filenumber,2]):
				plusarray[filenumber,2] = stopsite
				print("conservative")

##load start site
with open("/home/rf/Desktop/UTR/startcodon.csv", "rb") as csvfile:
        datareader = csv.reader(csvfile)
        count = 0
        for row in datareader:
		if count>=0:
			count+=1
			currenttxt = str(row)
			currentline = currenttxt.split("\\t")
  			genename = re.search('gene_name \"(.+?)\"',currenttxt).group(1)
			startsite = float(currentline[4])
			try:
				filenumber = int(numpy.where(plusarray == genename)[0])
				print(filenumber)
			except Exception, e:
				print("not found")
				continue
			if startsite > float(plusarray[filenumber,1]):
				plusarray[filenumber,1] = startsite
			

##doing the same for minus strand genes
with open("/home/rf/Desktop/UTR/startcodon.csv", "rb") as csvfile:
        datareader = csv.reader(csvfile)
        count = 0
        for row in datareader:
		if count>=0:
			count+=1
			currenttxt = str(row)
			currentline = currenttxt.split("\\t")
  			genename = re.search('gene_name \"(.+?)\"',currenttxt).group(1)
			startsite = float(currentline[3])
			try:
				filenumber = int(numpy.where(minusarray == genename)[0])
				print(stopsite)
			except Exception, e:
				print("not found")
				continue
			if minusarray[filenumber,1] == '0.0':
				minusarray[filenumber,1] = startsite
				print(minusarray[filenumber,1])
			elif startsite < float(minusarray[filenumber,1]):
				minusarray[filenumber,1] = startsite

with open("/home/rf/Desktop/UTR/stopcodon.csv", "rb") as csvfile:
        datareader = csv.reader(csvfile)
        count = 0
        for row in datareader:
		if count>=0:
			count+=1
			currenttxt = str(row)
			currentline = currenttxt.split("\\t")
  			genename = re.search('gene_name \"(.+?)\"',currenttxt).group(1)
			stopsite = float(currentline[4])
			try:
				filenumber = int(numpy.where(minusarray == genename)[0])
				print(stopsite)
			except Exception, e:
				print("not found")
				continue
			if stopsite > float(minusarray[filenumber,2]):
				minusarray[filenumber,2] = stopsite

##remove genes with too vague annotations (stop codon and start codon overlap)
counter = 0
for i in range(0,len(plusarray)):
	if float(plusarray[i,1])>=float(plusarray[i,2]):
		print(plusarray[i,0])
		plusarray[i,1]=0
		plusarray[i,2]=0
		counter+=1
counter
counter = 0
for i in range(0,len(minusarray)):
	if float(minusarray[i,1])<=float(minusarray[i,2]):
		print(minusarray[i,0])
		minusarray[i,1]=0
		minusarray[i,2]=0
		counter+=1
counter

##set output files
out3 = "/home/rf/Desktop/UTR/3UTR.gtf"
outfile = open(out3, 'a')
out5 = "/home/rf/Desktop/UTR/5UTR.gtf"
outfile2 = open(out5, 'a')

##filter UTR file
with open("/home/rf/Desktop/UTR/genes.gtf", "rb") as csvfile:
        datareader = csv.reader(csvfile)
        count = 0
	countthree = 0
	countfive = 0
        for row in datareader:
		currenttxt = str(row)
		printrow = row[0]
		currentline = currenttxt.split("\\t")
  		genename = re.search('gene_name \"(.+?)\"',currenttxt).group(1)
		strand = currentline[6]
		print(strand)
		if strand == '+':
			try:
				filenumber = int(numpy.where(plusarray == genename)[0])
			except Exception, e:
				print("not found")
				continue
			print(plusarray[filenumber])
			fivesite = float(currentline[3])
			threesite = float(currentline[4])
			print(str(fivesite) + "," + str(threesite))
			if (float(plusarray[filenumber,2]) <= fivesite and float(plusarray[filenumber,2])>0) or (float(plusarray[filenumber,2]) > fivesite and float(plusarray[filenumber,2]) < threesite and float(plusarray[filenumber,1]) < fivesite):
				for element in row:
					outfile.write(element)
				outfile.write("\n")
				print("3")
				countthree+=1
			elif float(plusarray[filenumber,1]) >= threesite or (float(plusarray[filenumber,1]) > fivesite and float(plusarray[filenumber,1]) < threesite and float(plusarray[filenumber,2]) > threesite):
				for element in row:
					outfile2.write(element)
				outfile2.write("\n")
				print("5")
				countfive+=1
		else:
			try:
				filenumber = int(numpy.where(minusarray == genename)[0])
				print(filenumber)
			except Exception, e:
				print("not found")
				continue
			print(minusarray[filenumber])
			fivesite = float(currentline[4])
			threesite = float(currentline[3])
			print(str(fivesite) + "," + str(threesite))
			if float(minusarray[filenumber,2]) >= fivesite or (float(minusarray[filenumber,2]) < fivesite and float(minusarray[filenumber,2]) > threesite and float(minusarray[filenumber,1]) > fivesite):
				for element in row:
					outfile.write(element)
				outfile.write("\n")
				print("3")
				countthree+=1
			elif (float(minusarray[filenumber,1]) <= threesite and float(minusarray[filenumber,1])>0) or (float(minusarray[filenumber,1]) > threesite  and float(minusarray[filenumber,1]) < fivesite and float(minusarray[filenumber,2]) < threesite):
				for element in row:
					outfile2.write(element)
				outfile2.write("\n")
				print("5")
				countfive+=1
		count+=1
		##if count >= 500:
		##	break
	outfile.close()
	outfile2.close()
print("out of " + str(count) + " UTR entries: " + str(countfive) + "  filed to 5', and " + str(countthree) + " filed to 3'.")
		
