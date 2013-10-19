import csv
import itertools
import geopy
import urllib2
from geopy import geocoders
from geopy.geocoders import googlev3


""" THE PROBLEM IS, I don't know how to add to a csv file on the row underneath the last- if you do, please fix :D """
def getCount(infile):
    i_f = open(infile, "r")
    return sum(1 for row in i_f)

def reverseGeo(streetAddress):
	"input a street address, output a tuple of latitude and longitude, many thanks to geopy -working "
	g = geocoders.GoogleV3()
	return g.geocode(streetAddress)[1]

def getaddress(infile, i):
    """Gets the address from the excel file"""
    i_f = open(infile, 'r')
    reader = csv.reader( i_f )
    e = -1
    for line in reader: 
        if e < i:
            e += 1
        else:
            return line[3] + "," + line[4] +","+ line[5]

def readOld(infile,i):
    i_f = open(infile, 'r')
    reader = csv.reader( i_f )
    e = -1
    for line in reader:
        if e < i:
            e += 1
        else:
            return line

def parse(infile, outfile): 
    """  working.... """
    
    of = open(outfile, "w")
    with open(outfile, 'a') as f1:
        for i in range(getCount(infile)):
            address = getaddress(infile,i)
            try:
                lat_lon = reverseGeo(address)
                new = readOld(infile, i)
                new.extend((str(lat_lon[0]), str(lat_lon[1])))
                new = ",".join(new)
                print new
                new = new.replace("\n","")
                of.write(new+"\n")
            except (urllib2.URLError,
geopy.geocoders.googlev3.GQueryError, geopy.geocoders.googlev3.GTooManyQueriesError, ValueError):
                row = readOld(infile,i)
                row.append('None')
     

parse("needToFix.csv", "fixed.csv")
