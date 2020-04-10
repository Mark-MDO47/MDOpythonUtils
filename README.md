# MDOpythonUtils
some short general purpose Python 3.x utilities

- xlsx2txt - create text form of values in \*.xls or \*.xlsx; allows quick comparison of files
  - example: `python xlsx2txt.py file.xlsx > file.txt`
  - reads the **values** from tabs/cells in file.xlsx (not formulas, formatting, etc.)
  - writes tab-separated-variable version to stdout in form `tabname\tA1\tA2\t...`
  - gotchas: has no real error checking; will barf on UnicodeEncodeError and other errors

- mdoUniq - 
  - example: `python mdoUniq.py fname.txt startStr endStr`
  - example: `grep -n StateValue debug.txt | python mdoUniq.py - : "at msec"`
  - performs simple uniq between startStr to endStr on each line
    - if startStr/endStr not found, boundaries are start/end of line
  - writes lines uniq between those two to stdout
  - useful for keeping line numbers but otherwise performing uniq
