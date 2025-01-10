# QRCode.py - make QR codes from instructions

```
usage: QRcode instructions

Reads the named instructions.txt file (tab-separated variable)
  and generates *.png QRcodes and *.html

positional arguments:
  instructions        path to instructions.txt file

options:
  -h, --help          show this help message and exit
  -d, --debug_output  enable debug output
  -s, --split_text    enable split text on |

NOTE: instructions.txt is filename.png<TAB>comment<TAB>text-for-QR-code
Example:
python QRcode.py instructions.txt
```
