# MDOpythonUtils
some short general purpose Python 3.x utilities

- xlsx2txt - create text form of values in \*.xls or \*.xlsx; allows quick comparison of files
  - example: `python xlsx2txt.py file.xlsx > file.txt`
  - reads the **values** from tabs/cells in file.xlsx (not formulas, formatting, etc.)
  - writes tab-separated-variable version to stdout in form `tabname\tA1\tA2\t...`
  - gotchas: has no real error checking; will barf on UnicodeEncodeError and other errors

- mdoUniq - uniq for part of the line
  - example: `python mdoUniq.py fname.txt startStr endStr`
  - example: `grep -n StateValue debug.txt | python mdoUniq.py - : "at msec"`
  - performs simple uniq between startStr to endStr on each line
    - if fname is "-", lines to compare are from stdin (allows pipe construct)
    - if "-i" or "--ignore-case" then ignore differences in case when comparing
    - comparison starts at first character of first instance of startStr
    - comparison stops before first character of first instance of endStr
    - if startStr|endStr not found, boundaries are start|end of line respectively
    - if startStr found after endStr, boundaries are entire line
  - writes lines uniq between those two to stdout
  - useful for keeping line numbers but otherwise performing uniq

- mdoAnsibleLint - start of a simple "lint" for Ansible YAML files
  - inspiration came from spending all day looking for a missing ":"
    - ansible-playbook, ansible-lint and yamllint were not leading me to the culprit
  - example: `python mdoAnsibleLint.py test.yml`
  - example: for v in \`find ansible_mdo -name "*.yml"\`; do python mdoAnsibleLint.py $v; done
  - -v, --verbose  always display contents of parsed YAML
  - at this time, just does yaml.load() then looks for missing ":" at first level

- ReadAmazonKindleList - start of routine to read Amazon Kindle list copied from website and make a spreadsheet
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
  - Example: `python ReadAmazonKindleList.py exampleKindleList.txt example_KindleBooks_Favorites.xlsx`
  - To check proper operation including switches, do `source testit.sh` in a GIT Bash or Linux environment. It does a "diff" at the end; if no further output then it matches.
    - `$ source testit.sh`
    - `opening D:\...\example_KindleBooks_Favorites.xlsx`
    - `opening D:\...\exampleKindleList.txt`
    - `opening D:\...\example_KindleBooks_Favorites.xlsx`
    - `opening D:\...\exampleKindleList.txt`
    - `opening D:\...\example_KindleBooks_Favorites.xlsx`
    - `opening D:\...\exampleKindleList.txt`
