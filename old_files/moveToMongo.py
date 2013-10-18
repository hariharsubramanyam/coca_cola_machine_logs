#! /usr/bin/env python
## -*- coding: utf-8 -*-

# usage: parser.py [-h] [--version] -i FILE -o FILE [-v]

import os
import sys
import glob
import numpy
import argparse
import ast
import time
import fileinput
from pymongo import MongoClient

def cleanLine(line):
    return line.strip().replace("\r","").split("\t")

def putFileIntoDatabase(in_file, mongo_client, database_name):
    print database_name
    db = mongo_client[database_name[0]]
    mongoIDForMachineID = {}
    i = 0
    machineIDs = {}
    for line in fileinput.input([in_file]):
        [machineID, timeStamp, sys_cmd, sys_sub_cmd, val1, val2, sys_text] =  cleanLine(line)
        if machineID in mongoIDForMachineID:
            objID = db.insert({"machineID":machineID, "logs":[(timeStamp, sys_cmd, sys_sub_cmd, val1, val2, sys_text)]})
            mongoIDForMachineID[machineID] = str(objID)
        else:
            db.update(query={"_id":machineID},
                    update={"$push",{"logs":(str(timeStamp), str(sys_cmd),
                        str(sys_sub_cmd), str(val1), str(val2), str(sys_text))}})        

def main():
# usage: parser.py [-h] [--version] -i FILE -o FILE [-v]
# 
# optional arguments:
#     -h, --help                        show this help message and exit
#                                                 output directory name
#     -i DIR, --input_file DIR
#                                                 input directory name
    # Parse line options.
    # Try to have always the same input options
    parser = argparse.ArgumentParser(description = 'parser')

    
    parser.add_argument("-i", "--input_file", nargs=1, required=True,
                    action = "store", dest="in_file",
                    help="input file name",
                    metavar='FILE')
                    
    parser.add_argument("-d", "--database_name", nargs=1, required=True,
            dest="database_name", default=None, help="name of mongodb database") 

    parser.add_argument("-u", "--mongodb_url", dest="mongodb_url", default=None,
                    help="url of the mongodb server")

    #Analysis of input parameters
    args = parser.parse_args()
    if args.mongodb_url is None:
        client = MongoClient()
    else:
        client = MongoClient(args.mongodb_url)

    if (not os.path.exists(args.in_file[0])):
            print "Error: Input file does not exist: ", args.in_file[0]
            exit()

    putFileIntoDatabase(args.in_file[0], client, args.database_name)
    return


        
## ##################################################
## ##################################################
## ##################################################

if __name__ == "__main__":
        main()

## ##################################################
## ##################################################
## ##################################################

