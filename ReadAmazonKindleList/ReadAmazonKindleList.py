# Author: Mark Olson 2021-10-01
#
# Amazon has a new format for their website
#
# copy text of your Kindle library to a *.txt file
# entries will look a little like this:
#
# King of Thorns (The Broken Empire Book 2)
# Mark Lawrence
# Acquired on September 24, 2021
# In2
# Collections
# 1
# Device
# Deliver or Remove from Device
# Mark as Read
# More actions
#
# The following may or may not be true anymore; the code still searches for it
# Disturbingly, sometimes the Kindle Library list will have a book more than once
# and sometimes it will not list a book that you actually have.
# I don't have a solution for that, but I do print some alerts.
# I have seen it list book 10 of a series two times and not list book 8.
#    When I searched the content for "Book 8", it found it.
#    When I cleared the search, it listed book 10 once and book 8 once.
#    I have code that will keep previously found books and if there are duplicates it keeps the first one with an alert.
# ... and sometimes they will change the Author name: they changed "Adrian Goldsworthy" to "Adrian Keith Goldsworthy"
#    There is some text output that might help alert you to this
#    flags --oldapproxmatch and --newapproxmatch are one way to help deal with it

import sys
# import string
import os
import argparse
import pandas as pd
# import datetime

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# special cases. Believe it or not, there are a bunch of normal cases too...
# [lcstring, series, seriesNum]
TITLE_totalMatch = []
TITLE_partialMatch = []
SUBSTITUTE_goofy = []
# do this substitution in 'Title', 'Author', 'Author (f,m,l)'
doSubstituteGoofy = ['Title', 'Author', 'Author (f,m,l)']


###################################################################################
# startOfLineIsIn()
#
#    theLine           - line to check
#    listOfCompares [] - strings to compare
#
def startOfLineIsIn(theLine, listOfCompares):
    startIsIn = False
    for compare in listOfCompares:
        if 0 == theLine.find(compare):
            startIsIn = True
            break
    return startIsIn

    # end of startOfLineIsIn()

###################################################################################
# doReadPreviousRatings()
#
# prevRatingsFname spreadsheet has tabs
#    Books                - previous version of our output spreadsheet
#                           save ratings, etc. and notice if we don't see one in listFname
#    TITLE_totalMatch     - if this matches total title then use series and seriesNum
#    TITLE_partialMatch   - if this matches any part of title then use series and seriesNum
# NOTE: titles in TITLE_totalMatch and TITLE_partialMatch are all made lower-case when we return
#
def doReadPreviousRatings(prevRatingsFname):
    prevRatings = {}
    # this was code for reading a tab-separated-variable version of tab 'Books'
    # df = pd.read_table(prevRatingsFname,sep='\t',encoding="cp1252") # I hate Windows smart quotes

    # Import the excel file
    sys.stderr.write("opening %s\n" % os.path.abspath(prevRatingsFname))
    xlsPd = pd.ExcelFile(prevRatingsFname)
    # xlsSheets = xlsPd.sheet_names

    # get special cases for a total title match - make them all lower case
    sheet = "TITLE_totalMatch"
    df = xlsPd.parse(sheet, header=0)
    for row in df.iterrows():
        if pd.isna(row['a']):
            break
        tmp = [row['a'].lower(), row['b'], row['c']]
        TITLE_totalMatch.append(tmp)
    del df

    # get special cases for a partial title match - make them all lower case
    sheet = "TITLE_partialMatch"
    df = xlsPd.parse(sheet, header=0)
    for i, row in df.iterrows():
        if pd.isna(row['a']):
            break
        tmp = [row['a'].lower(), row['b'], row['c']]
        TITLE_partialMatch.append(tmp)
    del df

    # get goofy character substitution list - do this substitution in 'Title', 'Author', 'Author (f,m,l)'
    sheet = "SUBSTITUTE_goofy"
    df = xlsPd.parse(sheet, header=0)
    for i, row in df.iterrows():
        if pd.isna(row['a']):
            break
        tmp = [row['a'], row['b']]
        SUBSTITUTE_goofy.append(tmp)
    del df

    # get the previous list of books with its ratings; do the goofy
    sheet = "Books"
    df = xlsPd.parse(sheet, header=0)
    # since the file exists, enter the "extra" headers; we merge this old data into the new list
    hdrs = ["FAV", "Rating", "re-check", "Read"]
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
                if hdr in doSubstituteGoofy:
                    for goofy in SUBSTITUTE_goofy:
                        tmp[hdr] = row[hdr].replace(goofy[0], goofy[1])
        theKey = row['Title']+"\t"+row['Author']
        if theKey in prevRatings:
            errmsg = "$$$ERROR$$$ %s found more than once in %s tab Books\n" % (theKey, prevRatingsFname)
            sys.stderr.write(errmsg)
            sys.stdout.write(errmsg)
        else:
            prevRatings[theKey] = tmp # Author matches authorRvrs below

    return prevRatings

    # end doReadPreviousRatings()

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

    # first translate goofy characters
    for goofy in SUBSTITUTE_goofy:
        title = title.replace(goofy[0], goofy[1])

    # Now this is a bit of a stretch: try to find the series and series number in title if possible
    # First handle special cases from the prevRatingsFname spreadsheet tabs
    foundSeries = False
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

    # end doProcessTitle()

###################################################################################
# doProcessAuthor - handle the author line
#
# Inputs:
#    theLine - line containing Author and (strangely) the date acquired; already .strip()
#
# return - author, authorRvrs
#    author - author as found on the input line: first (middle) last (suffix)
#    authorRvrs - author in last, first (middle)
#       NOTE: currently we don't handle suffixes (ex: Jr.)
#    dateAcquired - text of the date acquired
#
def doProcessAuthor(theLine, title):
    # second important line after dots is the author BUT...
    #    it is strangely concatenated with the date; remove the date
    author = theLine

    # first translate goofy characters
    for goofy in SUBSTITUTE_goofy:
        author = author.replace(goofy[0], goofy[1])

    # we have our best guess at the author in first last format; make the last, first format
    tmp = author.rfind(" ")
    if -1 != tmp:
        authorRvrs = author[tmp + 1:] + ", " + author[:tmp]
    else:
        authorRvrs = author # what are you supposed to do here?

    return author, authorRvrs

    # end doProcessAuthor()

###################################################################################
# doProcessDateAcquired - handle the Date Acquired line
#
# Inputs:
#    theLine - line containing the date acquired; already .strip()
#       example: Borrowed on July 23, 2021
#       example: Acquired on July 23, 2021
#
# return - dateAcquired
#    dateAcquired - text of the date acquired
#
def doProcessDateAcquired(theLine, title):
    # line after the author is the date acquired
    dateLine = theLine
    dateAcquired = ""

    # first translate goofy characters
    for goofy in SUBSTITUTE_goofy:
        dateLine = dateLine.replace(goofy[0], goofy[1])

    for month in MONTHS:
        tmp = dateLine.rfind(month)
        if -1 != tmp:
            dateAcquired = dateLine[tmp:]
            dateLine = dateLine[:tmp]
            break
    if 0 == len(dateAcquired):
        errmsg = "$$$ERROR$$$ - for title %s the line %s may not be dateLine; does not have a month\n" % (title, dateLine)
        sys.stdout.write(errmsg)
        sys.stderr.write(errmsg)

    return dateAcquired

    # end doProcessDateAcquired()

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

    # end checkApproxMatch()

###################################################################################
# makeKeyToPrevList() - make the key and check against previous list, possibly with approx match
#
# listFname is the path to listFname text file, copied from Kindle book list
# title is title of this book
# authorRvrs is LastnameFirstname
# approxMatchKeepAuthor is "No" for exact matches only on key between the two input files
#                         "Old" or "New" for approx matches allowed (approx match on author keyword, exact match title)
#                         Old author found in prevRatingsFname; New author found in listFname
# prevBooks
# approxPossibleMatchPrev [] if approxMatchKeepAuthor == "No", list possible approx matches
# approxMatchPrev [] if approxMatchKeepAuthor != "No", list possible approx matches
#
# Note: prevRatingsFname not actually used in this routine; refers to previous ratings *.xlsx spreadsheet
#
def makeKeyToPrevList(listFname, title, author, authorRvrs, approxMatchKeepAuthor, prevBooks, prevRatings, approxPossibleMatchPrev, approxMatchPrev):
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
    # if (approx ENabled) and (no exact match) and (yes approx match), "theKey" is now  approxKey
    if theKey in prevBooks:
        if 1 != prevBooks[theKey]:
            errmsg = "$$$ERROR$$$ %s found more than once in %s\n" % (theKey, listFname)
            sys.stderr.write(errmsg)
            sys.stdout.write(errmsg)
        prevBooks[theKey] = 0

    return theKey, approxGood, author, authorRvrs

    # end makeKeyToPrevList()

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
    approxGood = False # True if (approx ENabled) and (no exact match) and (yes approx match)
    title = ""  # book title
    author = "" # author in first last format
    authorRvrs = "" # author in last, first format
    series = "" # our attempt to detect the series that the book is a member of
    seriesNum = "" # our attempt to detect which book in the series this is
    didRead = ""  # tells if we read the book already - NOT IN THE NEW AMAZON FORMAT
    sawBlank = 0 # this is how we track that we reached another entry - NEW AMAZON FORMAT
        # 0 - waiting for first line of book
        # 1 - processed first line (title) waiting for second line
        # 2 - processed second line (author) waiting for third line
        # 3 - processed third line (date) waiting for blank line
    ignoreTextBlocks = ["Digital Content", "Mark as Read", "Showing ", "Deliver or Remove from Device"] # ignore block if starts with this

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
        # sys.stderr.write("%s\n" % theLine)
        if 0 == len(theLine): # end of text block
            sawBlank = 0
            series = ""
            seriesNum = ""
            didRead = ""  # tells if we read the book already - that info not in new AMAZON format
        elif 0 == sawBlank:
            # first line after blank lines is the title
            if startOfLineIsIn(theLine, ignoreTextBlocks):
                sawBlank = 3 # ignore the entire text block
            else:
                title, series, seriesNum = doProcessTitle(theLine)
                sawBlank += 1
        elif 1 == sawBlank:
            # second line is the author
            author, authorRvrs = doProcessAuthor(theLine, title)

            # make the key and adjust matches and possible matches
            theKey, approxGood, author, authorRvrs = makeKeyToPrevList(listFname, title, author, authorRvrs,
                        approxMatchKeepAuthor, prevBooks, prevRatings, approxPossibleMatchPrev, approxMatchPrev)
            sawBlank += 1
        elif 2 == sawBlank:
            # third and last line we care about is the dateAcquired
            dateAcquired = doProcessDateAcquired(theLine, title)

            # all done with this entry; print result and get ready for next entry
            # first print the columns from listFname
            sys.stdout.write(
                "%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % (title, authorRvrs, author, series, seriesNum, didRead, dateAcquired))
            # then print out columns from match or approx match
            if theKey in prevRatings:
                for col in mergeHdrs:
                    sys.stdout.write("%s\t" % prevRatings[theKey][col])
            elif False == approxGood:
                noMatchPrev.append(theKey)
                for hdr in mergeHdrs:
                    sys.stdout.write("\t")
            sys.stdout.write("\n")

            # start search for next entry but we did not yet see blank
            sawBlank += 1
            series = ""
            seriesNum = ""
            didRead = ""  # tells if we read the book already - that info not in new AMAZON format
        elif 3 == sawBlank: # shouldn't get here but just in case further code mods made
            if 0 == len(theLine):
                sawBlank = 0 # now look for next book
        theLine = fptr.readline() # get the next line and do the while check

    # clean out special entries in prevBooks with column headers
    # NOTE - python says cannot pop() when doing 'for aKey in hdrsOnly:' - that changes dictionary & continues looping
    prevBooks.pop(hdrsOnly[0]) # this is not a book
    prevBooks.pop(hdrsOnly[1]) # this is not a book
    if 2 != len(hdrsOnly): # just a warning if we get more headers, need to change code above (sigh)
        errmsg = "$$$ERROR$$$ expected hdrsOnly length 2 is length %d" % len(hdrsOnly)
        sys.stderr.write(errmsg)
        sys.stdout.write(errmsg)

    # any books in listFname have already been output
    # if any books were in prevRatingsFname but not in listFname
    #    first add them to the normal output above so we don't lose them
    #    then notify user
    # copy books to end of output that were not found in listFname but found in prevRatingsFname
    for theKey in prevBooks.keys():
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
                    try:
                        sys.stdout.write("%s\t" % prevRatings[theKey][col])
                    except:
                        sys.stderr.write("\nERROR on col |%s|\n" % (col))
                        sys.stderr.flush()
                        sys.stderr.write("%s\n" % prevRatings[theKey])
                        sys.stderr.flush()
                        # sys.stderr.write("\nERROR on key |%s|\n" % (theKey))
                        # sys.stderr.write("%s\n" % prevRatings[theKey])
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

   # end of doReadAmazonKindleList()

###################################################################################
# "__main__" processing for ReadAmazonKindleList
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
    me_group = my_parser.add_mutually_exclusive_group(required=False)
    me_group.add_argument('-n',
                           '--newapproxmatch',
                           action='store_true',
                           help='accepts approx matches in the two input files and preserves new Author; default is exact matches')
    me_group.add_argument('-o',
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

    # end of "__main__"
