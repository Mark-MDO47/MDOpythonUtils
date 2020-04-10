#
# mdoUniq.py - my crude "uniq" for comparing only between start and end strings
#
# Author: Mark Olson 2019-12-21
#

import sys
import io
import argparse

def mdoUniq(fname, startStr, endStr):
   if '-' == fname:
       fobj = sys.stdin
   else:
       fobj = open(fname, 'rt')
   prevLine = ""
   theLine = fobj.readline()
   while "" != theLine: # null string means EOF
      theLine = theLine.strip()
      nStart = theLine.find(startStr)
      nEnd = theLine.find(endStr)
      # if could not find startStr and/or endStr, default to start or end of line
      if (-1 == nStart):
         nStart = 0
      if (-1 == nEnd):
         nEnd = len(theLine)
      if prevLine != theLine[nStart:nEnd]:
          # theLine differes from prevLine, print it
         print("%s" % theLine)
      prevLine = theLine[nStart:nEnd]
      theLine = fobj.readline()
   fobj.close()

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='mdoUniq',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="simple uniq between startStr to endStr on each line",
        epilog="""Example: suppose mdo.txt has the following lines

<<<other lines>>>
28:DEBUG loop() - nowVinputRBG 0x100 msec 1085
<<<other lines>>>
47:DEBUG loop() - nowVinputRBG 0x100 msec 1139
<<<other lines>>>
112:DEBUG loop() - nowVinputRBG 0x4500 msec 1374
<<<other lines>>>
600:DEBUG loop() - nowVinputRBG 0x4500 msec 4757
<<<other lines>>>
965:DEBUG loop() - nowVinputRBG 0x4501 msec 6172

This will find those DEBUG lines that changed somewhere between the D of DEBUG and the m of msec:

$ grep DEBUG mdo.txt | python mdoUniq.py - DEBUG msec
28:DEBUG loop() - nowVinputRBG 0x100 msec 1085
112:DEBUG loop() - nowVinputRBG 0x4500 msec 1374
965:DEBUG loop() - nowVinputRBG 0x4501 msec 6172
""",
        usage='%(prog)s fname startStr endStr',)
    my_parser.add_argument('fname',type=str,help='path to file to perform mdoUniq on; "-" for stdin')
    my_parser.add_argument('startStr',type=str,help='string marking start of uniq comparison')
    my_parser.add_argument('endStr',type=str,help='string marking end of uniq comparison')
    args = my_parser.parse_args()

    mdoUniq(args.fname, args.startStr, args.endStr)

