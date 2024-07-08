# ReadAmazonKindleList

ReadAmazonKindleList - start of routine to read Amazon Kindle list copied from website and make a spreadsheet
- For usage text: `python ReadAmazonKindleList.py -h`
- Input spreadsheet and stdout have columns for favorites, ratings, and re-check that get copied from the old books spreadsheet
- example: `python ReadAmazonKindleList.py list.txt prevRatings.xlsx  > formattedList.txt`
  - list.txt is path to text file, copied from Kindle book list
  - prevRatings.xlsx is path to previous ratings *.xlsx spreadsheet in tab "Books"
  - formattedList.txt is tab-separated-variable list
- NOTE: **exampleKindleList.txt** shows the list.txt format obtained from copying out of the Amazon website
- NOTE: **example_KindleBooks_Favorites.xlsx** is an example of my "prevRatings.xslx"
- prevRatings.xlsx spreadsheet has tabs
  - Books                - previous version of our output spreadsheet
  - TITLE_totalMatch     - if this matches total title then use series and seriesNum
  - TITLE_partialMatch   - if this matches any part of title then use series and seriesNum
  - SUBSTITUTE_goofy - a list of goofy characters from UTF or Windows and what to replace them with
- Example: `python ReadAmazonKindleList.py exampleKindleList.txt example_KindleBooks_Favorites.xlsx`
- To check proper operation including switches, do `source testit.sh` in a GIT Bash or Linux environment. It does a "diff" at the end; if no further output then it matches.
  - `$ source testit.sh`
  - `opening D:\...\example_KindleBooks_Favorites.xlsx`
  - `opening D:\...\exampleKindleList.txt`
  - `opening D:\...\example_KindleBooks_Favorites.xlsx`
  - `opening D:\...\exampleKindleList.txt`
  - `opening D:\...\example_KindleBooks_Favorites.xlsx`
  - `opening D:\...\exampleKindleList.txt`
  
Sometimes the Kindle Library list will have a book more than once
- and sometimes it will not list a book that you actually have.
- I don't have a solution for that, but I do print some alerts.

I have seen it list book 10 of a series two times and not list book 8.
- When I searched the content for "Book 8", it found it.
- When I cleared the search, it listed book 10 once and book 8 once.
- I have code that will keep previously found books and if there are duplicates it keeps the first one with an alert.

And sometimes they will change the Author name: they changed "Adrian Goldsworthy" to "Adrian Keith Goldsworthy"
- There is some text output that might help alert you to this
- flags --oldapproxmatch and --newapproxmatch are one way to help deal with it

The sort order I use for this spreadsheet is as follows:
- sort by Author, Series, Num, Title
- sort anything that looks like a number as a number
