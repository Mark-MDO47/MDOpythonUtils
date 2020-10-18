# xlsx2txt

xlsx2txt - create text form of values in \*.xls or \*.xlsx; allows quick comparison of files
- example: `python xlsx2txt.py file.xlsx > file.txt`
- reads the **values** from tabs/cells in file.xlsx (not formulas, formatting, etc.)
- writes tab-separated-variable version to stdout in form `tabname\tA1\tA2\t...`
- gotchas: has no real error checking; will barf on UnicodeEncodeError and other errors

`$ python xlsx2txt.py -h`
- usage: xlsx2txt spreadsheet
- stdout receives tab-separated-values form of data in *.xls or *.xlsx
- positional arguments:
  - spreadsheet  path to spreadsheet.xls or spreadsheet.xlsx
- optional arguments:
  - -h, --help   show this help message and exit
- Example:
  - python xlsx2txt.py old.xlsx > old.txt
  - python xlsx2txt.py new.xlsx > new.txt
  - diff old.txt new.txt
