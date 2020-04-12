#
# mdoUniq.py - my crude "uniq" for comparing only between start and end strings
#
# Author: Mark Olson 2019-12-21
#
# This trivial code must have been written dozens of times in various languages, but I needed a version for myself.
#
# mdoUniq - uniq for part of the line
#
# example: python mdoUniq.py fname.txt startStr endStr
# example: grep -n StateValue debug.txt | python mdoUniq.py - : "at msec"
# performs simple uniq between startStr to endStr on each line
#  - if fname is "-", lines to compare are from stdin (allows pipe construct)
#  - if "-i" or "--ignore-case" then ignore differences in case when comparing
#  - comparison starts at first character of first instance of startStr
#  - comparison stops before first character of first instance of endStr
#  - if startStr|endStr not found, boundaries are start|end of line respectively
#  - if startStr found after endStr, boundaries are entire line
#  - writes lines uniq between those two to stdout
# useful for keeping line numbers but otherwise performing uniq
# allows checking just the middle portion of the line for uniqueness
#

import sys
# import io
import argparse

def doMdoUniq(fname, fobjOtp, startStr, endStr, ignoreCase):
    numLines = 0
    if '-' == fname:
        fobjInp = sys.stdin
    else:
        fobjInp = open(fname, 'rt')

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
            numLines += 1
        prevLine = compareLine[nStart:nEnd]
        theLine = fobjInp.readline()

    fobjInp.close()

    return numLines

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


    doMdoUniq(args.fname, sys.stdout, args.startStr, args.endStr, args.ignore_case)
