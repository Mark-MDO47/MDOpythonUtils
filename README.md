# MDOpythonUtils
**Some short general purpose Python 3.x utilities**

**Table Of Contents**
* [Top](#mdopythonutils "Top")
* [create_md_TOC - read GitHub-style MarkDown and insert Table of Contents](#create_md_toc-\--read-github\-style-markdown-and-insert-table-of-contents "create_md_TOC - read GitHub-style MarkDown and insert Table of Contents")
* [xlsx2txt - create text form of values in .xls or .xlsx - allows quick comparison of files](#xlsx2txt-\--create-text-form-of-values-in-xls-or-xlsx-\--allows-quick-comparison-of-files "xlsx2txt - create text form of values in .xls or .xlsx - allows quick comparison of files")
* [mdoUniq - uniq for part of the line](#mdouniq-\--uniq-for-part-of-the-line "mdoUniq - uniq for part of the line")
* [mdoAnsibleLint - start of a simple lint for Ansible YAML files](#mdoansiblelint-\--start-of-a-simple-lint-for-ansible-yaml-files "mdoAnsibleLint - start of a simple lint for Ansible YAML files")
* [ReadAmazonKindleList - Read Amazon Kindle list copied from website and make a spreadsheet](#readamazonkindlelist-\--read-amazon-kindle-list-copied-from-website-and-make-a-spreadsheet "ReadAmazonKindleList - Read Amazon Kindle list copied from website and make a spreadsheet")
* [ProcessPhotos - sort Google Photos downloads by date/time](#processphotos-\--sort-google-photos-downloads-by-datetime "ProcessPhotos - sort Google Photos downloads by date/time")
* [DirectoryWalk - Traverse 2 Directory Trees and Describe Differences](#directorywalk-\--traverse-2-directory-trees-and-describe-differences "DirectoryWalk - Traverse 2 Directory Trees and Describe Differences")
* [CDRipRename - renames CD RIP fnames to longer names based on trackname file](#cdriprename-\--renames-cd-rip-fnames-to-longer-names-based-on-trackname "CDRipRename - renames CD RIP fnames to longer names based on trackname file")

## create_md_TOC - read GitHub-style MarkDown and insert Table of Contents
- example: python create_md_TOC.py README.md
- reads the input file and inserts table of contents at marker "\*\*Table Of Contents\*\*"
- gotchas: handles several special characters (-?!:/.) but not all

## xlsx2txt - create text form of values in .xls or .xlsx - allows quick comparison of files
- example: `python xlsx2txt.py file.xlsx > file.txt`
- reads the **values** from tabs/cells in file.xlsx (not formulas, formatting, etc.)
- writes tab-separated-variable version to stdout in form `tabname\tA1\tA2\t...`
- gotchas: has no real error checking; will barf on UnicodeEncodeError and other errors

## mdoUniq - uniq for part of the line
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

## mdoAnsibleLint - start of a simple lint for Ansible YAML files
- inspiration came from spending all day looking for a missing ":"
  - ansible-playbook, ansible-lint and yamllint were not leading me to the culprit
- example: `python mdoAnsibleLint.py test.yml`
- example: for v in \`find ansible_mdo -name "*.yml"\`; do python mdoAnsibleLint.py $v; done
- -v, --verbose  always display contents of parsed YAML
- at this time, just does yaml.load() then looks for missing ":" at first level

## ReadAmazonKindleList - Read Amazon Kindle list copied from website and make a spreadsheet
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
  - SUBSTITUTE_goofy     - a list of goofy characters from UTF or Windows and what to replace them with
- for the Match tabs, upper/lower case is ignored in the match
- Example: `python ReadAmazonKindleList.py exampleKindleList.txt example_KindleBooks_Favorites.xlsx`
- To check proper operation including switches, do `source testit.sh` in a GIT Bash or Linux environment. It does a "diff" at the end; if no further output then it matches.
  - `$ source testit.sh`
  - `opening D:\...\example_KindleBooks_Favorites.xlsx`
  - `opening D:\...\exampleKindleList.txt`
  - `opening D:\...\example_KindleBooks_Favorites.xlsx`
  - `opening D:\...\exampleKindleList.txt`
  - `opening D:\...\example_KindleBooks_Favorites.xlsx`
  - `opening D:\...\exampleKindleList.txt`

## ProcessPhotos - sort Google Photos downloads by date/time
- tools to sort photos downloads
  - stdout receives bash shell script to set filedates and filename
- tools to convert heic to jpeg
- gotchas: has not been extensively tested

## DirectoryWalk - Traverse 2 Directory Trees and Describe Differences
- For usage text: `python DirectoryWalk.py -h`
- Example: `python DirectoryWalk.py "D:\path-to-my\StuffAndInterests" X > DirectoryCompareInfo.txt`
- File compare options: --cmp_ignore, --cmp_length_date, --cmp_sha256

## CDRipRename - renames CD RIP fnames to longer names based on trackname file
- For usage text: `python CDRipRename.py -h`
- Example: `python CDRipRename.py -s CD -nd 3 SoundForgeTextFile.txt | sed "s?F_Chopin?Chopin?"`
- Options: --numdigits NUMDIGITS, --startwith STARTWITH, --use_leading_tracnum
