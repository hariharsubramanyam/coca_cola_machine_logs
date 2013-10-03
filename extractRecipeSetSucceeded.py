import sys

if __name__=="__main__":
    inF = open(sys.argv[1], "r")
    outF = open(sys.argv[2], "w")
    k = 0
    for line in inF:
        k += 1
        splitLine = line.split('\t')
        if k > 1 and int(splitLine[2]) == 1002:
            outF.write(line)
    inF.close()
    outF.close()
