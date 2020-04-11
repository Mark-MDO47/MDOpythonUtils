#
# mdoUniq.py - my crude "uniq" for comparing only between start and end strings
#
# Author: Mark Olson 2019-12-21
#

import sys
# import io
import argparse

def mdoUniq(fobjInp, fobjOtp, startStr, endStr, ignoreCase):
    if ignoreCase:
        startStr = startStr.upper()
        endStr = endStr.upper()
    # print("startStr |%s| endStr |%s|" % (startStr,endStr))
    prevLine = ""
    theLine = fobjInp.readline()
    while "" != theLine: # null string means EOF
        compareLine = theLine = theLine.strip()
        if ignoreCase:
            compareLine = theLine.upper()
        nStart = compareLine.find(startStr)
        nEnd = compareLine.find(endStr)
        # print("compareLine |%s| nStart=%d nEnd=%d" % (compareLine, nStart, nEnd))
        if -1 == nStart:
            # if startStr not found, then comparison starts at beginning of line
            nStart = 0
        if -1 == nEnd:
            # if endStr not found, then comparison stops at end of line
            nEnd = len(theLine)
        if nEnd < nStart:
            # if endStr is found before startStr then comparison uses entire line
            nStart = 0
            nEnd = len(theLine)
        if prevLine != compareLine[nStart:nEnd]:
            # theLine differs from prevLine, print it
            fobjOtp.write("%s\n" % theLine)
        prevLine = compareLine[nStart:nEnd]
        theLine = fobjInp.readline()

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='mdoUniq',
        formatter_class=argparse.RawTextHelpFormatter,
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
    my_parser.add_argument('startStr',type=str,help="""string marking start of uniq comparison
    comparison starts at first character of first instance of startStr
    if startStr not found, then comparison starts at beginning of line
""")
    my_parser.add_argument('endStr',type=str,help="""string marking end of uniq comparison
    comparison stops before first character of first instance of endStr
    if endStr not found, then comparison stops at end of line
    if endStr is found before startStr then comparison uses entire line
    """)
    my_parser.add_argument('-i',
                           '--ignore-case',
                           action='store_true',
                           help='ignore differences in case when comparing')
    args = my_parser.parse_args()

    # opening the file here makes unit test easier
    if '-' == args.fname:
        fobjInp = sys.stdin
    else:
        fobjInp = open(args.fname, 'rt')

    mdoUniq(fobjInp, sys.stdout, args.startStr, args.endStr, args.ignore_case)

    fobjInp.close()
