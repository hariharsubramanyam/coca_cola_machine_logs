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

## ######

## ##################################################
## ##################################################
def Cparser(in_file,out_file,verbose):

  tps1 = time.clock()
  ## INITIALIZATION
  kompt=dict();
  desc=dict();

  ## TREAT DATA
  for line in fileinput.input([in_file]):
    line = line.strip() # removes \n
    line = line.replace('\r','')
    line = line.split('\t')
    if len(line)>2:
      if line[2] not in kompt:
        kompt[line[2]]=0;
        desc[line[2]]=line[6];
      kompt[line[2]] +=1; 


  ## ORDER
  S_kompt = kompt.items()
  S_kompt.sort(cmpval)

  ## OUTPUT
  f_out = open(out_file, "w")
  f_out.write("NUMBER\tID\tLABEL\n\n");
  #
  for elm in S_kompt:
    f_out.write("%d\t%s\t%s\n" % (kompt[elm[0]],elm[0],desc[elm[0]]));
  f_out.close()

  ## END
  tps2 = time.clock()
  print("%f" % (tps2-tps1));

  return

## ##################################################
def cmpval(x,y):
    if x[1]>y[1]:
        return -1
    elif x[1]==y[1]:
        return 0
    else:
        return 1

## ##################################################
## ##################################################
## ##################################################

def main():
# usage: parser.py [-h] [--version] -i FILE -o FILE [-v]
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   --version             show program's version number and exit
#   -o DIR, --output_file DIR
#                         output directory name
#   -i DIR, --input_file DIR
#                         input directory name
  # Parse line options.
  # Try to have always the same input options
  parser = argparse.ArgumentParser(description = 'parser')

  parser.add_argument('--version', action='version', version='%(prog)s 1.1')
  
  parser.add_argument("-i", "--input_file", nargs=1, required=True,
          action = "store", dest="in_file",
          help="input file name",
          metavar='FILE')
          
  parser.add_argument("-o", "--output_file", nargs=1, required=True,
          action = "store", dest="out_file",
          help="output file name",
          metavar='FILE')

  parser.add_argument("-v", "--verbose",
          action = "store_true", dest="verbose",
          default = False,
          help="verbose mode [default %(default)s]")

  #Analysis of input parameters
  args = parser.parse_args()
  
  if (not os.path.exists(args.in_file[0])):
      print "Error: Input file does not exist: ", args.in_file[0]
      exit()


  ##      
  Cparser(args.in_file[0],args.out_file[0],args.verbose)

  return


    
## ##################################################
## ##################################################
## ##################################################

if __name__ == "__main__":
    main()

## ##################################################
## ##################################################
## ##################################################

