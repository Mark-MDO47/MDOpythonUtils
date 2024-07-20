# Author: Mark Olson 2024-06-15
#
# JazzBooks.py - reads a text file from Amazon list of 63 Jazz books
#
# Creates table of contents in tab-separated-variable format
#
# Restriction - text file comes from Amazon website
#
# Note: I think these are all Hal Leonard books
#
import sys
# import string
# import re as re # had a little trouble with regular expressions
# import os
import argparse

MATCH_TITLE_STRING = "Solos"
MATCH_VOL_STRINGS = [ " Volume ", " Vol. ", " Solos, " ]
STATE_SKIP_TO_BLANK_LINE = 1 # skip to a blank line
STATE_SEARCH_FOR_TITLE   = 2 # search for title

###################################################################################
# do_title_line(a_line)
#
def do_title_line(a_line):
    vol_string = "NONE"
    for test_vol_string in MATCH_VOL_STRINGS:
        if -1 != a_line.find(test_vol_string):
            vol_string = test_vol_string
            break
    if "NONE" == vol_string:
        # sys.stderr.write("Could not find volume in %s\n" % a_line)
        vol_num_string = "NONE"
    else:
        tmp = len(vol_string) + a_line.rfind(vol_string)
        vol_num_string = ""
        while (tmp < len(a_line)) and a_line[tmp].isdigit():
            vol_num_string += a_line[tmp]
            tmp += 1
    sys.stdout.write("%s\t%s\n" % (vol_num_string, a_line))



###################################################################################
def do_JazzBooks(fname):
    our_state = STATE_SEARCH_FOR_TITLE
    prev_line = ""
    fobj = open(fname, 'r')
    a_line = fobj.readline()
    while 0 != len(a_line):
        prev_line = a_line
        a_line = a_line.rstrip()
        if (0 == len(a_line)) or ("$" == a_line[0]): # blank line or price, find next title
            our_state = STATE_SEARCH_FOR_TITLE
        elif (-1 != a_line.find(MATCH_TITLE_STRING)) and (STATE_SEARCH_FOR_TITLE == our_state):
            do_title_line(a_line)
            our_state = STATE_SKIP_TO_BLANK_LINE
        a_line = fobj.readline()
    fobj.close()
    # end do_JazzBooks()

###################################################################################
# "__main__" processing for JazzBooks
#
# use argparse to process command line arguments
# python JazzBooks.py -h to see what the arguments are
#
if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='JazzBooks',
        formatter_class=argparse.RawTextHelpFormatter,
        description="reads a text (*.txt) file andand writes TSV lines to stdout a table of contents",
        epilog="""Example:
python JazzBooks.py ListOfBooks_jazzPiano_RAW.txt > ListOfBooks_jazzPiano_TSV.txt
""",
        usage='%(prog)s fname')
    my_parser.add_argument('fname',type=str,help='path to list of books text file')
    args = my_parser.parse_args()

    do_JazzBooks(args.fname)