# Author: https://github.com/Mark-MDO47 2024-12-23
#
# QRcode.py - reads named file "instructions.txt"
#   generates QR codes
#
# When used to generate QR codes for the UniRemoteCYD program, it should
#     make an output as described below:
# https://github.com/Mark-MDO47/UniRemote/
#
########################### INPUT ###########################
# The input QR code file should be a tab-separated-variable text file
#     of the following form:
# <*.png filename><TAB><DESCRIPTION STRING><TAB><MAC ADDRESS><"|"><COMMAND STRING>
#
# Most of those fields are described in the output section.
# The ones for input only are here.
#
# <*.png filename> is a string giving a unique filename for the generated QR-code.
#     The *.png will be created containing a QR code in the output format below.
#     There will also be a *.html file to display the QR code in a browser
#      example: bad_test_lg_msg.png
#
# <"|"> is the single character of a vertical bar (the bash pipe character).
#
#
########################### OUTPUT ###########################
# The output QR code or MIFARE Classic EV1 1K card should be a
#     tab-separated-variable text file of the following form:
# <MAC ADDRESS><TAB><COMMAND STRING><TAB><DESCRIPTION STRING>
# 
# <MAC ADDRESS> is a string of the following exact form:
#     ##:##:##:##:##:##
#   This is the MAC Address that will be used to send the ESP-NOW message;
#     the MAC address of the target system.
#   Note that this is a six-part MAC address in hexadecimal. Each hex number
#   is exactly two digits long. If you need to start it with a zero, do so.
#   Because I am a lazy coder, formatting the string properly is up to you.
# 
# <COMMAND STRING> is a short (maximum 249 characters + zero termination) command
#   The receiving MAC address will receive it as a zero-terminated string (including
#   the zero terminator).
#
# <DESCRIPTION STRING> can be zero length or more, but for consistency
#   the <TAB> prior to the description string is required.
#   The description is just for your purposes; it is not sent to the ESP-NOW target.

import qrcode
import sys
# import os
import argparse


###################################################################################
# do_QRcode() - read instructions from fname; make QR code files
#
def do_QRcode(fname, debug_output, split_text):
    fmt = '<img src="%s" width="400" alt="%s" style="max-width: 100%s;"><br><br>\n\n\n'
    # my_cwd = os.getcwd()

    # my old-style text reading
    fobj = open(fname, 'rt')
    a_line = fobj.readline()
    while 0 != len(a_line):
        # process the line for validity checking
        line_good = True
        a_line = a_line.strip()
        if debug_output:
            sys.stderr.write("%s\n" % a_line)
        a_split_tmp = a_line.split("\t")
        a_split = []
        for t in a_split_tmp:
            a_split.append(t.strip())

        # validity check the line
        if 3 > len(a_split):
            sys.stderr.write("  $$$ ERROR $$$: instruction must have 3 tab-separated fields, not %d<br><br>\n\n" % len(a_split))
            line_good = False
        elif 4 != (len(a_split[0]) - a_split[0].find(".png")):
            sys.stderr.write("  $$$ ERROR $$$: QR filename must be *.png not '%s'<br><br>\n\n" % a_split[0])
            line_good = False
        elif (-1 != a_split[0].find("\\")) or (-1 != a_split[0].find("/")):
            sys.stderr.write("  $$$ ERROR $$$: QR filename not change directories as in '%s'<br><br>\n\n" % a_split[0])
            line_good = False

        if line_good:        
            # make QR code
            img = qrcode.make(a_split[2]) # [2] is text for QR code
            img.save(a_split[0])          # [0] is filename
            fout = open(a_split[0][:-3] + "html", 'wt')
            tmp = -1
            if split_text:
                tmp = a_split[2].find("|")
            fout.write("<H1>%s : %s</H1><br><br>\n" % (a_split[1], a_split[2][tmp+1:]))
            fout.write(fmt % (a_split[0],a_split[1],"%"))
            fout.close()
        
        # read next lline
        a_line = fobj.readline()
    fobj.close()
    sys.stdout.write("All done.\n")
    # end do_QRcode()


###################################################################################
# "__main__" processing for QRcode
#
# use argparse to process command line arguments
# python QRcode.py -h to see what the arguments are
#
if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='QRcode',
        formatter_class=argparse.RawTextHelpFormatter,
        description="Reads the named instructions.txt file (tab-separated variable)\n  and generates *.png QRcodes and *.html",
        epilog="""NOTE: instructions.txt is filename.png<TAB>comment<TAB>text-for-QR-code
Example:
python QRcode.py instructions.txt
""",
        usage='%(prog)s instructions')
    my_parser.add_argument('instructions',type=str,help='path to instructions.txt file')
    my_parser.add_argument('-d', '--debug_output', action='store_true', help='enable debug output')
    my_parser.add_argument('-s', '--split_text', action='store_true', help='enable split text on |')
    args = my_parser.parse_args()

    do_QRcode(args.instructions, args.debug_output, args.split_text)