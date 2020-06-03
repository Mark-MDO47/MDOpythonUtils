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
