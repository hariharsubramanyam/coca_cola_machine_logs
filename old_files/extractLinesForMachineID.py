import sys

if __name__=="__main__":
    machineID = sys.argv[1]
    inF = open(sys.argv[2], "r")
    outF = open(sys.argv[3], "wb")
    for line in inF:
        l = line.rstrip("\n\r").replace("\r","")
        splitLine = l.split("\t")
        splitLine[0] = splitLine[0].replace('"', '')
        if splitLine[0] == machineID:
            outF.write(l + "\n")
    inF.close()
    outF.close()
