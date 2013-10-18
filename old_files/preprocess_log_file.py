import fileinput
import sys
import re
import datetime
import time

in_file = sys.argv[1]
firstLine = True
regexMatch = r"(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)"
baseTime = datetime.datetime(year=1970, month=1, day=1)
for line in fileinput.FileInput(in_file,inplace=1):
	if firstLine:
		line = line.replace("dspn_ser_nbr", "machineID")
		line = line.replace("sys_log_tmst", "timestamp")
		line = line.replace("sys_log_msg_cd", "actionID")
		line = line.replace("sys_log_msg_sub_cd", "subActionID")
		line = line.replace("sys_log_msg_val1", "ingredientID")
		line = line.replace("sys_log_msg_val2", "val2")
		line = line.replace("sys_log_msg_txt", "log")
		line += "\tquantity"
	line=line.replace("\r","").replace('"','').replace('\n','')
	split_line = line.split('\t')
	pattern = re.compile(regexMatch)
	m = pattern.match(split_line[1])
	if(m):
		dateObj = datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6)))
		line = line.replace(m.group(0), str(int((dateObj - baseTime).total_seconds())))
	if (not firstLine) and int(split_line[2]) == 5042 and len(split_line) < 8:
		description = split_line[6]
		mL = int(description[description.find("Now")+3:description.find("mL")])
		line += "\t" + str(mL)
	elif not firstLine:
		line += "\t" + "-1"
	if firstLine:
		firstLine = False
	print line
