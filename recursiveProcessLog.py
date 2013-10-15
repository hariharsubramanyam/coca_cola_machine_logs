#! /usr/bin/env python
## -*- coding: utf-8 -*-


'''
Recursively walks through CocaCola FreeStyle machine log files and reformats the
files for a mongoimport

The input log files (the name of the file is the machineID) take the form (tab
separated)
# comment
# comment
...
# comment

MM/DD/YYYY  HH:MM:SS    SYSCMD  SYSSUBCMD   VAL1    VAL2    SYSTEXT
MM/DD/YYYY  HH:MM:SS    SYSCMD  SYSSUBCMD   VAL1    VAL2    SYSTEXT
...
MM/DD/YYYY  HH:MM:SS    SYSCMD  SYSSUBCMD   VAL1    VAL2    SYSTEXT

The script makes the following changes:
    Replaces MM/DD/YYYY HH:MM:SS with a timestamp
    If SYSCMD == 5042:
        this means the SYSTEXT takes the form
        IHM: Ingredient fuel gauge changed. Now XXX mL See
        [ingredientID,busHdl].
        
        so we extract XXX and append it to the end of the string
    Else:
        apends -1 to the end of the string
'''
import os
import sys
import glob
import numpy
import argparse
import ast
import time
import fileinput
import re
import datetime

datePattern = re.compile("(\d\d)/(\d\d)/(\d\d\d\d)")
timePattern = re.compile("(\d\d):(\d\d):(\d\d)")
baseTime = datetime.datetime(year=1970, month=1, day=1)
# Recursively walk through all the files contained within "startDirectory"
# and execute logProcess on them
def recursiveLogProcess(startDirectory):
    for dirpath, dnames, fnames in os.walk(startDirectory):
        for f in fnames:
            # first parameter is the file path, second parameter is the machine
            # name 
            if f[0] == '.':
                continue
            print "Processing",f
            sys.stdout.flush()
            logProcess(os.path.join(dirpath, f), dirpath[dirpath.rfind('/')+1:])
            os.system("mongoimport --db testDB --collection freestyleLogs --type tsv --file " + os.path.join(dirpath,f) + " --fields type,machineID,timeStamp,actionID,subActionID,ingredientID,val2,actionDescription,quantity")
# Given a file path with the machine logs and the machine name,
# Create the
def logProcess(fpath, machineName):
    f = open(fpath,"r")
    for line in fileinput.FileInput(fpath, inplace=1):
        if len(line) < 5 or line[0] == "#": 
            continue
        line = line.replace("\r\n", "")
        split_line = line.split("\t")
        (theDate, theTime, syscmd, syssubcmd, val1, val2, description) = split_line 
        dateMatch = datePattern.match(theDate)
        timeMatch = timePattern.match(theTime)
        (month, day, year) = (int(dateMatch.group(1)), int(dateMatch.group(2)), int(dateMatch.group(3)))
        (hours, mins, secs) = (int(timeMatch.group(1)), int(timeMatch.group(2)), int(timeMatch.group(3)))
        dateObj = datetime.datetime(year, month, day, hours, mins, secs)
        replaceMe = split_line[0] + "\t" + split_line[1]
        line = "log\t" + machineName + "\t" + line.replace(replaceMe, str(int((dateObj - baseTime).total_seconds())))
        if int(syscmd) == 5042:
            mL = int(description[description.find("Now")+3:description.find("mL")])
            line += "\t" + str(mL)
        else:
            line += "\t-1"
        print line

    f.close()

def main():
# usage: recursiveProcessLog.py [-h] -i STARTDIR 
# 
# optional arguments:
#     -h, --help                        show this help message and exit
#     -i STARTDIR, --input_file STARTDIR
#                                                 input directory name
    # Parse line options.
    # Try to have always the same input options
    parser = argparse.ArgumentParser(description = 'parser')

    parser.add_argument('--version', action='version', version='%(prog)s 1.1')
    
    parser.add_argument("-i", "--input_directory", nargs=1, required=True,
                    action = "store", dest="in_dir",
                    help="input directory name",
                    metavar='FILE')
                    
    #Analysis of input parameters
    args = parser.parse_args()
    
    if (not os.path.exists(args.in_dir[0])):
            print "Error: Input directory does not exist: ", args.in_dir[0]
            exit()
    recursiveLogProcess(args.in_dir[0])
    return

if __name__ == "__main__":
        main()
