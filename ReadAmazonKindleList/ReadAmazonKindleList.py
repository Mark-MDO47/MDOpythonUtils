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
#    I have code that will keep previously found books and if there are duplicates it keeps the first one with warning.
# ... and sometimes they will change the Author name: they changed "Adrian Goldsworthy" to "Adrian Keith Goldsworthy"
#    There is some text output that might help you discover this
#    flags --oldapproxmatch and --newapproxmatch are one way to deal with it

import sys
import string
import os
import argparse
import pandas as pd
import datetime

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# special cases. Believe it or not, there are a bunch of normal cases too...
# [lcstring, series, seriesNum
TITLE_totalMatch = []
TITLE_partialMatch = []

###################################################################################
# doReadPreviousRatings()
#
# prevRatingsFname spreadsheet has tabs
#    Books                - previous version of our output spreadsheet
#                           save ratings, etc. and notice if we don't see one in listFname
#    TITLE_totalMatch     - if this matches total title then use series and seriesNum
#    TITLE_partialMatch   - if this matches any part of title then use series and seriesNum
#
def doReadPreviousRatings(prevRatingsFname):
    prevRatings = {}
    # this was code for reading a tab-separated-variable version of tab 'Books'
    # df = pd.read_table(prevRatingsFname,sep='\t',encoding="cp1252") # I hate Windows smart quotes

    # Import the excel file
    sys.stderr.write("opening %s\n" % os.path.abspath(prevRatingsFname))
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
    # since the file exists, enter the "extra" headers; we merge this old data into the new list
    hdrs = ["FAV", "Rating", "re-check"]
    prevRatings["prevRatingsMergeHdrs"] = hdrs
    bkHdrs = df.columns.values
    prevRatings["prevRatingsAllHdrs"] = bkHdrs

    for i, row in df.iterrows():
        if pd.isna(row['Title']):
            break
        tmp = {}
        for i, hdr in enumerate(bkHdrs):
            if pd.isna(row[hdr]):
                tmp[hdr] = ""
            else:
                tmp[hdr] = row[hdr]
        theKey = row['Title']+"\t"+row['Author']
        if theKey in prevRatings:
            errmsg = "$$$ERROR$$$ %s found more than once in %s tab Books\n" % (theKey, prevRatingsFname)
            sys.stderr.write(errmsg)
            sys.stdout.write(errmsg)
        else:
            prevRatings[theKey] = tmp # Author matches authorRvrs below

    return prevRatings

###################################################################################
# doProcessTitle(theLine) - handle the title line; attempt to extract the series and seriesNum
#
# Inputs:
#    theLine - line containing tile; already .strip()
#
# return - title, series, seriesNum
#    title - set to theLine
#    series - either "" or a book series name
#    seriesNum - either text of a number or (special cases) a sub-title
#
def doProcessTitle(theLine):
    # first line after dots is the title
    title = theLine
    series = ""
    seriesNum = ""

    # Now this is a bit of a stretch: try to find the series and series number in title if possible
    # First handle special cases from the prevRatingsFname spreadsheet tabs
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

    # if didn't match special case, look for (series name book #) or (volume...)
    if (False == foundSeries) and ((-1 != title.rfind("Book ")) or (-1 != title.rfind("Volume "))):
        tmpBk = title.rfind("Book ")
        if -1 == tmpBk:
            tmpBk = title.rfind("Volume ")
        numBk = title[tmpBk:]
        tmpSeries = title[:tmpBk].strip()
        tmpStr = numBk[1 + numBk.find(" "):]
        if tmpStr.lower() == "one":
            tmpStr = "1"  # sometimes they say "one" for the first one; go figure...
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
        if (len(series) - 1) == series.find(","):  # if series name ends with "," remove it
            series = series[:series.find(",")]
        tmp = series.lower()
        if (0 == tmp.find("the ")) and (
                0 != tmp.find("the way")):  # if series name starts with "the ", remove unless "the way"
            series = series[4:]
        elif 0 == tmp.find("a "):  # if series name starts with "a ", remove
            series = series[2:]
        elif "april series" == tmp:  # combine "april series" and "april"
            series = "April"

    # now clean up a little for pretty printout
    # prevent series number of 1.0
    seriesNum = str(seriesNum)
    tmp = seriesNum.find(".")
    if -1 != tmp:
        seriesNum = seriesNum[:tmp]

    return title, series, seriesNum

###################################################################################
# doProcessAuthor - handle the author line
#
# Inputs:
#    theLine - line containing Author and (strangely) the date acquired; already .strip()
#
# return - author, authorRvrs, dateAcquired
#    author - author as found on the input line: first (middle) last (suffix)
#    authorRvrs - author in last, first (middle)
#       NOTE: currently we don't handle suffixes (ex: Jr.)
#    dateAcquired - text of the date acquired
#
def doProcessAuthor(theLine):
    # second important line after dots is the author BUT...
    #    it is strangely concatenated with the date; remove the date
    author = theLine
    dateAcquired = ""

    for month in MONTHS:
        tmp = author.rfind(month)
        if -1 != tmp:
            break
    if -1 != tmp:
        dateAcquired = author[tmp:]
        author = author[:tmp]
    else:
        errmsg = "$$$ERROR$$$ - for title %s the line %s may not be author; does not have a month\n" % (title, author)
        sys.stdout.write(errmsg)
        sys.stderr.write(errmsg)

    # we have our best guess at the author in first last format; make the last, first format
    tmp = author.rfind(" ")
    if -1 != tmp:
        authorRvrs = author[tmp + 1:] + ", " + author[:tmp]
    else:
        authorRvrs = author # what are you supposed to do here?

    return author, authorRvrs, dateAcquired

###################################################################################
# checkApproxMatch - determine if there is an approximate match
#
# Inputs:
#    theKey - key (title\tauthor) for exact match
#    prevBooks - 
#
# return approxGood, theKey
#    approxGood - true if (not exact match) and (approximate match)
#    approxKey - key (title\tauthor) for approx match else ""
#
def checkApproxMatch(theKey, prevBooks):
    approxGood = False

    approxKey = ""
    splitTheKey = theKey.split("\t")
    title = splitTheKey[0]
    author = splitTheKey[1]
    
    if theKey not in prevBooks:
        # approx = exact title match and approx match in author
        authorSplit = author.replace(",", "").split(" ")
        for chkKey in prevBooks:
            if -1 != chkKey.find(title):
                for chkAuth in authorSplit:
                    if (len(chkAuth) <= 1) or ((2 == len(chkAuth)) and ("." == chkAuth[1])):
                        continue  # ignore those tiny cases such as initials
                    if -1 != chkKey.find(chkAuth):
                        approxGood = True  # author matches approximately (partially)
                        approxKey = chkKey
                        break
                if approxGood:
                    break
    return approxGood, approxKey



###################################################################################
# doReadAmazonKindleList() - print new Kindle tab-separated-variable spreadsheet
#
# listFname is text file copied from Amazon website for Kindle contents
# prevRatingsFname spreadsheet has tabs
#    Books                - previous version of our output spreadsheet
#                           save ratings, etc. and notice if we don't see one in listFname
#    TITLE_totalMatch     - if this matches total title then use series and seriesNum
#    TITLE_partialMatch   - if this matches any part of title then use series and seriesNum
# approxMatchKeepAuthor is "No" for exact matches only on key between the two input files
#                         "Old" or "New" for approx matches allowed (approx match on author keyword, exact match title)
#                         Old author found in prevRatingsFname; New author found in listFname
#
def doReadAmazonKindleList(listFname, prevRatingsFname, approxMatchKeepAuthor):
    noMatchPrev = [] # list of keys when no match or approx match with previous
    approxMatchPrev = [] # if approxMatchKeepAuthor != "No", list possible approx matches
    approxPossibleMatchPrev = [] # if approxMatchKeepAuthor == "No", list possible approx matches
    title = ""  # book title
    author = "" # author in first last format
    authorRvrs = "" # author in last, first format
    series = "" # our attempt to detect the series that the book is a member of
    seriesNum = "" # our attempt to detect which book in the series this is
    sawDots = 0 # this is how we track that we reached another entry

    # prevRatings is a dictionary with "title\tauthor": for now [FAV, Rating, re-check]
    # title "prevRatingsMergeHdrs" will give the headers
    prevRatings = doReadPreviousRatings(prevRatingsFname)
    prevBooks = dict.fromkeys(prevRatings, 1) # we expect to find 1 copy of each book in listFname

    # open the Amazon List file; it will tell us if that is a problem
    sys.stderr.write("opening %s\n" % os.path.abspath(listFname))
    fptr = open(listFname, 'rt')

    # since the file exists, print the header
    #    hdrsOnly[]: list of column entries in prevRatings for headers:
    #        allHdrs: "prevRatingsAllHdrs" for all the headers we track
    #        mergeHdrs: "prevRatingsMergeHdrs" for the ones we merge (personal ratings) from prevRatings to output
    hdrsOnly = ["prevRatingsAllHdrs", "prevRatingsMergeHdrs"]
    allHdrs = prevRatings["prevRatingsAllHdrs"]
    mergeHdrs = prevRatings["prevRatingsMergeHdrs"]
    for hdr in allHdrs:
        sys.stdout.write("%s\t" % hdr)
    sys.stdout.write("\n")

    # our old-fashioned method to read listFname (a text file) line by line
    theLine = fptr.readline()
    while 0 != len(theLine):
        theLine = theLine.strip()
        if (len(theLine) > 0) and ("READ" != theLine) and ("Update Available" != theLine): # don't pay attention to READ or Update Available
            if 1 == sawDots:
                # first line after dots is the title
                title, series, seriesNum = doProcessTitle(theLine)
                sawDots += 1
            elif 2 == sawDots:
                # second important line after dots is the author BUT...
                #    it is strangely concatenated with the date; remove the date
                author, authorRvrs, dateAcquired = doProcessAuthor(theLine)

                # Now make the key to prevRatingsFname (and prevBooks) and see if it is there with exact match
                #     if it doesn't match and approx is enabled, look for approximate match
                #     if it doesn't match and approx is disabled, look anyway to give a warning
                theKey = title+"\t"+authorRvrs # key is title+tab+author where author is "lastname, firstname ..."
                approxGood = False # True if (approx ENabled) and (no exact match) and (yes approx match)
                approxPossible = False # True if (approx DISabled) and (no exact match) and (yes approx match)
                approxPossibleKey = "" # non-null if approxPossible True

                if ("No" != approxMatchKeepAuthor) and (theKey not in prevBooks):
                    # approx = exact title match and approx match in author
                    approxGood, approxKey = checkApproxMatch(theKey, prevBooks)
                    if approxGood:
                        # (approx ENabled) and (no exact match) and (yes approx match)
                        approxMatchPrev.append("OLD\t" + approxKey + "\tapprox match to NEW\t" + theKey)
                        theKey = approxKey
                        if "Old" == approxMatchKeepAuthor:
                            author = prevRatings[theKey]["Author (f,m,l)"]
                            authorRvrs = prevRatings[theKey]["Author"]
                elif "No" == approxMatchKeepAuthor:
                    # just want to know if it is possible even though they didn't ask for it
                    approxPossible, approxPossibleKey = checkApproxMatch(theKey, prevBooks)
                    if approxPossible:
                        # (approx Disabled) and (no exact match) and (yes approx match)
                        approxPossibleMatchPrev.append("OLD\t" + approxPossibleKey + "\tis POSSIBLE approx match to NEW\t" + theKey)

                # check that we only match betweeen listFname and prevRatingsFname one time
                # if (approx ENabled) and (no exact match) and (yes approx match), theKey is approx key
                if theKey in prevBooks:
                    if 1 != prevBooks[theKey]:
                        errmsg = "$$$ERROR$$$ %s found more than once in %s\n" % (theKey, listFname)
                        sys.stderr.write(errmsg)
                        sys.stdout.write(errmsg)
                    prevBooks[theKey] = 0

                # all done; print result and get ready for next entry
                sys.stdout.write("%s\t%s\t%s\t%s\t%s\t%s\t" % (title, authorRvrs, author, series, seriesNum, dateAcquired))
                if theKey in prevRatings:
                    for col in mergeHdrs:
                        sys.stdout.write("%s\t" % prevRatings[theKey][col])
                elif False == approxGood:
                    noMatchPrev.append(theKey)
                    for hdr in mergeHdrs:
                        sys.stdout.write("\t")
                sys.stdout.write("\n")
                sawDots = 0
                series = ""
                seriesNum = ""
        if "..." == theLine:
            sawDots = 1
        theLine = fptr.readline() # get the next line and do the while check

    # clean out special entries in prevBooks with column headers
    # NOTE - python says cannot pop() when doing 'for aKey in hdrsOnly:' - that changes dictionary & continues looping
    prevBooks.pop(hdrsOnly[0]) # this is not a book
    prevBooks.pop(hdrsOnly[1]) # this is not a book
    if 2 != len(hdrsOnly):
        errmsg = "$$$ERROR$$$ expected hdrsOnly length 2 is length %d" % len(hdrsOnly)
        sys.stderr.write(errmsg)
        sys.stdout.write(errmsg)

    # any books in listFname have already been output
    # if any books were in prevRatingsFname but not in listFname
    #    first add them to the normal output above so we don't lose them
    #    then notify user
    # copy books to end of output that were not found in listFname but found in prevRatingsFname
    for theKey in prevBooks:
        if 1 == prevBooks[theKey]:
            for col in allHdrs:
                if "Num" == col:
                    # prevent series number of 1.0
                    seriesNum = str(prevRatings[theKey][col])
                    tmp =  seriesNum.find(".")
                    if -1 != tmp:
                        seriesNum = seriesNum[:tmp]
                    sys.stdout.write("%s\t" % seriesNum)
                elif "DateAcq" == col:
                    # don't include " 00:00:00" that we get from reading *.xlsx
                    if (str(type(prevRatings[theKey][col])) == "<class \'pandas._libs.tslibs.timestamps.Timestamp\'>") or \
                            (str(type(prevRatings[theKey][col])) == "<class 'datetime.datetime'>"):
                        sys.stdout.write("%s\t" % prevRatings[theKey][col].strftime("%B %d, %Y"))
                    else:
                        sys.stdout.write("%s\t" % prevRatings[theKey][col])
                else:
                    sys.stdout.write("%s\t" % prevRatings[theKey][col])
            sys.stdout.write("\n")

    # notify user if any books were in prevRatingsFname but not in listFname
    print("\n\nThese books were in %s but not in %s; copied in at end above" % (prevRatingsFname, listFname))
    for theKey in prevBooks:
        if 1 == prevBooks[theKey]:
            print("%s" % theKey)

    # notify user if any books were in listFname but not in prevRatingsFname
    print("\n\nFYI These books were new in %s, not in %s" % (listFname, prevRatingsFname))
    for nomatch in noMatchPrev:
        print(nomatch)


    # notify user of any approximate matches, whether they asked for approx or not
    if "No" != approxMatchKeepAuthor:
        print("\n\nFYI These NEW books were an approximate match in %s and in %s; treated as a match since --%sapproxmatch flag used" % (listFname, prevRatingsFname, approxMatchKeepAuthor.lower()))
        for theApproxMatch in approxMatchPrev:
            print(theApproxMatch)
    else:
        print("\n\nFYI These NEW books were an approximate match in %s and in %s; NOT treated as a match since neither --...approxmatch flag used (new or old)" % (listFname, prevRatingsFname))
        for theApproxMatch in approxPossibleMatchPrev:
            print(theApproxMatch)


###################################################################################
# "main" processing for ReadAmazonKindleList
#
# use argparse to process command line arguments
# python ReadAmazonKindleList.py -h to see what the arguments are
#
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
    my_group = my_parser.add_mutually_exclusive_group(required=False)
    my_parser.add_argument('-n',
                           '--newapproxmatch',
                           action='store_true',
                           help='accepts approx matches in the two input files and preserves new Author; default is exact matches')
    my_parser.add_argument('-o',
                           '--oldapproxmatch',
                           action='store_true',
                           help='accepts approx matches in the two input files and preserves old Author; default is exact matches')
    args = my_parser.parse_args()

    # transmogrify user flags for approxmatch
    approxMatchKeepAuthor = "No"
    if args.newapproxmatch:
        approxMatchKeepAuthor = "New"
    elif args.oldapproxmatch:
        approxMatchKeepAuthor = "Old"

    # all the real work is done here
    doReadAmazonKindleList(args.listFname, args.prevRatingsFname, approxMatchKeepAuthor)