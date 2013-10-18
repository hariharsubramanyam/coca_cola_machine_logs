import fileinput
import sys

in_file = sys.argv[1]
for line in fileinput.FileInput(in_file,inplace=1):
	if len(line) < 2:
		continue
	line=line.replace('"','').replace('\n','')
	print line