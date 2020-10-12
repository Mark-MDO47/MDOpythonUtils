# Author: Mark Olson 2020-10-04
#
# copy text of your Kindle library to a *.txt file
# entries will look a little like this:
#     ...
#     The Dirty Streets of Heaven (Bobby Dollar Book 1)
#     READ
#     Tad WilliamsMarch 2, 2018
#     1
#     1
#
# There might or might not be a "READ" or a "Update Available"
# The author has a date following the name (strangely)
#
# Disturbingly, sometimes the Kindle Library list will have a book more than once
# and sometimes it will not list a book that you actually have.
# I don't have a solution for that.
# I have seen it list book 10 of a series two times and not list book 8.
#    When I searched the content for "Book 8", it found it.
#    When I cleared the search, it listed book 10 once and book 8 once.
#    Hmmm...

import sys
import string
import os
import argparse
import pandas as pd

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# special cases. Believe it or not, there are a bunch of normal cases too...
# [lcstring, series, seriesNum
TITLE_totalMatch = []
TITLE_partialMatch = []


def doReadPreviousRatings(prevRatingsFname):
    prevRatings = {}
    hdrs = ["FAV", "Rating", "re-check"]
    prevRatings["prevRatingsHdrs"] = hdrs

    # df = pd.read_table(prevRatingsFname,sep='\t',encoding="cp1252") # I hate Windows smart quotes
    # print(df.head(3))

    # Import the excel file
    xlsPd = pd.ExcelFile(prevRatingsFname)
    xlsSheets = xlsPd.sheet_names

    # get special cases for a total title match
    sheet = "TITLE_totalMatch"
    df = xlsPd.parse(sheet, header=0)
    for i, row in df.iterrows():
        if pd.isna(row['a']):
            break
        tmp = [row['a'], row['b'], row['c']]
        TITLE_totalMatch.append(tmp)
    del df

    # get special cases for a partial title match
    sheet = "TITLE_partialMatch"
    df = xlsPd.parse(sheet, header=0)
    for i, row in df.iterrows():
        if pd.isna(row['a']):
            break
        tmp = [row['a'], row['b'], row['c']]
        TITLE_partialMatch.append(tmp)
    del df

    # get the previous list of books with its ratings
    sheet = "Books"
    df = xlsPd.parse(sheet, header=0)
    for i, row in df.iterrows():
        if pd.isna(row['Title']):
            break
        tmp = []
        for i, hdr in enumerate(hdrs):
            if pd.isna(row[hdr]):
                tmp.append("")
            else:
                tmp.append(row[hdr])
        thekey = row['Title']+"\t"+row['Author']
        #if -1 != thekey.find("Strange Dogs"):
        #    print("$$$FOUND$$$ %s" % thekey)
        prevRatings[thekey] = tmp # Author matches authorRvrs below

    return prevRatings

def doReadAmazonKindleList(listFname, prevRatingsFname):
    noMatchPrev = []
    sawDots = 0 # this is how we track that we reached another entry
    title = ""
    author = "" # author in first last format
    authorRvrs = "" # author in last, first format
    series = "" # our attempt to detect the series that the book is a member of
    seriesNum = "" # our attempt to detect which book in the series this is

    # prevRatings is a dictionary with "title": for now [FAV, Rating, re-check]
    # title "prevRatingsHdrs" will give the headers
    prevRatings = doReadPreviousRatings(prevRatingsFname)

    # open the Amazon List file; it will tell us if that is a problem
    sys.stderr.write("opening %s\n" % os.path.abspath(listFname))
    fptr = open(listFname, 'rt')

    # since the file exists, print the header
    sys.stdout.write("Title\tAuthor\tAuthor (f,m,l)\tSeries\tNum")
    theHdrs = prevRatings["prevRatingsHdrs"]
    for hdr in theHdrs:
        sys.stdout.write("\t%s" % hdr)
    sys.stdout.write("\n")

    # our old-fashioned method to read a text file line by line
    theLine = fptr.readline()
    while 0 != len(theLine):
        theLine = theLine.strip()
        if ("READ" != theLine) and ("Update Available" != theLine): # don't pay attention to READ or Update Available
            if (len(theLine) > 0) and (0 != sawDots):
                if 1 == sawDots:
                    # first line after dots is the title
                    title = theLine
                    series = ""
                    seriesNum = ""

                    # now this is a bit of a stretch: try to find the series and series number if possible
                    foundSeries = False;
                    title_lower = title.lower()
                    for totMatch in TITLE_totalMatch:
                        if totMatch[0] == title_lower:
                            series = totMatch[1]
                            seriesNum = totMatch[2]
                            foundSeries = True
                            break
                    if (False == foundSeries):
                        for partMatch in TITLE_partialMatch:
                            if -1 != title_lower.find(partMatch[0]):
                                series = partMatch[1]
                                seriesNum = partMatch[2]
                                foundSeries = True
                                break

                    if (False == foundSeries) and ((-1 != title.rfind("Book ")) or (-1 != title.rfind("Volume "))):
                        tmpBk = title.rfind("Book ")
                        if -1 == tmpBk:
                            tmpBk = title.rfind("Volume ")
                        numBk = title[tmpBk:]
                        tmpSeries = title[:tmpBk].strip()
                        tmpStr = numBk[1+numBk.find(" "):]
                        if tmpStr.lower() == "one":
                            tmpStr = "1" # sometimes they say one for the first one; go figure...
                        numBk = ""
                        for tmp in range(len(tmpStr)):
                            if False == tmpStr[tmp].isdigit():
                                break
                            numBk += tmpStr[tmp]
                        if 0 != len(numBk):
                            if -1 != tmpSeries.rfind("("):
                                series = tmpSeries[1 + tmpSeries.rfind("("):]
                                seriesNum = numBk

                        # now it gets really special case ; don't judge me ;^)
                        if (len(series)-1) == series.find(","): # if series name ends with "," remove it
                            series = series[:series.find(",")]
                        tmp = series.lower()
                        if (0 == tmp.find("the ")) and (0 != tmp.find("the way")): # if series name starts with "the ", remove unless "the way"
                            series = series[4:]
                        elif 0 == tmp.find("a "):# if series name starts with "a ", remove
                            series = series[2:]
                        elif "april series" == tmp: # combine "april series" and "april"
                            series = "April"
                    sawDots += 1
                elif 2 == sawDots:
                    # second important line after dots is the author BUT...
                    #    it is strangely concatenated with the date; remove the date
                    author = theLine
                    for month in MONTHS:
                        tmp = author.rfind(month)
                        if -1 != tmp:
                            break
                    if -1 != tmp:
                        author = author[:tmp]
                    else:
                        errmsg = "ERROR - for title %s the line %s may not be author; does not have a month" % (title, author)
                        print(errmsg)
                        sys.stderr.write("%s\n" % errmsg)

                    # we have our best guess at the author in first last format; make the last, first format
                    tmp = author.rfind(" ")
                    authorRvrs = author[tmp+1:] + ", " + author[:tmp]

                    # all done; print result and get ready for next entry
                    sys.stdout.write("%s\t%s\t%s\t%s\t%s" % (title, authorRvrs, author, series, seriesNum))
                    thekey = title+"\t"+authorRvrs
                    #if -1 != thekey.find("Strange Dogs"):
                    #    print("$$$FOUND$$$ %s" % thekey)
                    if thekey in prevRatings:
                        for tmp in prevRatings[thekey]:
                            sys.stdout.write("\t%s" % tmp)
                    else:
                        noMatchPrev.append(thekey)
                        for hdr in theHdrs:
                            sys.stdout.write("\t")
                    sys.stdout.write("\n")
                    sawDots = 0
                    series = ""
                    seriesNum = ""
        if "..." == theLine:
            sawDots = 1
        theLine = fptr.readline() # get the next line and do the while check

    print("\n\nThese books were new, not in prev")
    for nomatch in noMatchPrev:
        print(nomatch)



if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='ReadAmazonKindleList',
        formatter_class=argparse.RawTextHelpFormatter,
        description="stdout receives tab-separated-values form of data from listFname",
        epilog="""Example:
python ReadAmazonKindleList.py list.txt prevRatings.xlsx  > formattedList.txt
""",
        usage='%(prog)s listFname prevRatingsFname')
    my_parser.add_argument('listFname',type=str,help='path to listFname text file, copied from Kindle book list')
    my_parser.add_argument('prevRatingsFname',type=str,help='path to previous ratings *.xlsx spreadsheet')
    args = my_parser.parse_args()

    doReadAmazonKindleList(args.listFname, args.prevRatingsFname)