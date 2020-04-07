#
# mdoUniq.py - my crude "uniq" for comparing only between start and end strings
#
# Author: Mark Olson 2019-12-21
#

import sys
import io
import argparse

def mdoUniq(fname, startStr, endStr):
   prevLine = ""
   fobj = open(fname, 'rt')
   theLine = fobj.readline()
   while "" != theLine: # null string means EOF
      theLine = theLine.strip()
      # print("DEBUG - line.strip() |%s|" % theLine)
      nStart = theLine.find(startStr)
      nEnd = theLine.find(endStr)
      if (-1 == nStart):
         nStart = 0
      if (-1 == nEnd):
         nEnd = len(theLine)
      if prevLine != theLine[nStart:nEnd]:
         print("%s" % theLine)
      prevLine = theLine[nStart:nEnd]
      # read the next line
      theLine = fobj.readline()
   fobj.close()

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='mdoUniq',
        description="simple uniq between startStr to endStr on each line",
        usage='%(prog)s fname startStr endStr',)
    my_parser.add_argument('fname',type=str,help='path to file to perform mdoUniq on')
    my_parser.add_argument('startStr',type=str,help='string marking start of uniq comparison')
    my_parser.add_argument('endStr',type=str,help='string marking end of uniq comparison')
    args = my_parser.parse_args()

    mdoUniq(args.fname, args.startStr, args.endStr)