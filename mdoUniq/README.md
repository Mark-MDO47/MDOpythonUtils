# mdoUniq

mdoUniq - uniq for part of the line
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

`$ python mdoUniq.py -h`
- usage: mdoUniq fname startStr endStr
- simple uniq between startStr to endStr on each line
- positional arguments:
  - fname              path to file to perform mdoUniq on; "-" for stdin
  - startStr           string marking start of uniq comparison
    - comparison starts at first character of first instance of startStr
    - if startStr not found, then comparison starts at beginning of line
  - endStr             string marking end of uniq comparison
    - comparison stops before first character of first instance of endStr
    - if endStr not found, then comparison stops at end of line
    - if endStr is found before startStr then comparison uses entire line
- optional arguments:
  - -h, --help         show this help message and exit
  - -i, --ignore-case  ignore differences in case when comparing
- **Example**: suppose mdo.txt has the following lines
- <<< other lines >>>
- 28:DEBUG loop() - nowVinputRBG 0x100 msec 1085
- <<< other lines >>>
- 47:DEBUG loop() - nowVinputRBG 0x100 msec 1139
- <<< other lines >>>
- 112:DEBUG loop() - nowVinputRBG 0x4500 msec 1374
- <<< other lines >>>
- 600:DEBUG loop() - nowVinputRBG 0x4500 msec 4757
- <<< other lines >>>
- 965:DEBUG loop() - nowVinputRBG 0x4501 msec 6172
- **Then** this will find those DEBUG lines that changed somewhere between the D of DEBUG and the m of msec:
- `$ grep DEBUG mdo.txt | python mdoUniq.py - DEBUG msec`
- `28:DEBUG loop() - nowVinputRBG 0x100 msec 1085`
- `112:DEBUG loop() - nowVinputRBG 0x4500 msec 1374`
- `965:DEBUG loop() - nowVinputRBG 0x4501 msec 6172`

Note that line 47: is missing since it does not change between the D of DEBUG and the m of msec
