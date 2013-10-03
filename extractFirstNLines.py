import sys

if __name__=="__main__":
    numLines = int(sys.argv[1])
    inF = open(sys.argv[2], "r")
    outF = open(sys.argv[3], "wb")
    k = 0
    for line in inF:
        l = line.rstrip("\n\r").replace("\r","")
        k += 1
        outF.write(l + "\n")
        if k > numLines:
            break
    inF.close()
    outF.close()
