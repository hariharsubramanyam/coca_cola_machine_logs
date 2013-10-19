import csv
import itertools
import geopy
import urllib2
import simplejson as json
import sys
import time

def reverseGeo(streetAddress):
    url = "http://www.datasciencetoolkit.org/street2coordinates/"
    for x in streetAddress[0].split(' '):
        url += x+"+"
    for x in streetAddress[1].split(' '):
        url += x + "+"
    for x in streetAddress[2].split(' '):
        url += x + "+"
    url += ""
    print url
    try:
        response = urllib2.urlopen(url).read()
        dat = json.loads(str(response)).values()[0]
        return (dat['latitude'], dat['longitude'])
    except:
        return (url,  None)
def parse(infile, outfile):
    """  working.... """
    lines = open(infile,"r").readlines()
    of = open(outfile, "w")
    erf = open("error.txt","w")
    numLines = 1.0*len(lines)
    k = 0
    shouldRun = True
    for i in range(1, len(lines)):
        line = lines[i]
        k += 1
        split_line = line.split(",")
        address = (split_line[3], split_line[4], split_line[5])
        (lat, lon) =  reverseGeo(address)
        if lon is None:
            erf.write(line)
            continue
        address = split_line[0] + "," + split_line[1] + "," + split_line[2] + "," +  split_line[3] + "," + split_line[4] + "," +  split_line[5]+ "," + split_line[6] + "," + str(lat) + "," + str(lon)
        of.write(address+"\n")
        print k, "of", numLines, "completed"
        print
        sys.stdout.flush()
    of.close()

parse("needToFix.txt", "fixed.txt")
#parse("FreestyleDispensers.csv", "FreestyleDispensersReadyForImport.csv")
