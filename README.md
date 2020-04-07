# MDOpythonUtils
some short general purpose Python 3.x utilities

- ExpandXls - create text form of values in \*.xls or \*.xlsx; allows quick comparison of files
  - example: `python ExpandXls.py file.xlsx > file.txt`
  - reads the **values** from tabs/cells in file.xlsx (not formulas, formatting, etc.)
  - writes tab-separated-variable version to stdout in form `tabname\tA1\tA2\t...`
  - gotchas: has no real error checking; will barf on UnicodeEncodeError and other errors

- mdoUniq - 
  - example: `python mdoUniq fname.txt startStr endStr`
  - performs simple uniq between startStr to endStr on each line
  - writes lines uniq between those two to stdout
  - useful for keeping line numbers but otherwise performing uniq
