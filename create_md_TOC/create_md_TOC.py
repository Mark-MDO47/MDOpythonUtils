# Author: Mark Olson 2023-09-28
#
# create_md_TOC.py - reads a MarkDown (*.md) file and creates a
#   table of contents
#
# restriction - the only special character processed is "-"
#

import sys
# import string
import re as re
# import os
import argparse

"""
C_PREPROC_DIRECTIVES = [
        "#include ",
        "#pragma ",
        "#define ",
        "#undef ",
        "#error ",
        "#warning ",
        "#if ",
        "#else ",
        "#elif ",
        "#endif ",
        "#ifdef ",
        "#ifndef ",
        "#line "
    ]


###################################################################################
# false_if_preproc - return False if C Preprocessor Directive
#
#
def false_if_preproc(a_line):
    found = True
    my_line = a_line.lstrip()
    for preproc in C_PREPROC_DIRECTIVES:
        if 0 == my_line.find(preproc):
            found = False
            break
    return found
    # end false_if_preproc()
"""

###################################################################################
# do_create_md_TOC - do the work
#
#
def do_create_md_TOC(fname):
    re_ptrn = re.compile('^#[#]* ')
    found_top = False
    found_toc = -1
    save_lines = []
    toc_lines = []
    line_end = "" # will use line end we find in file

    toc_lines.append("**Table Of Contents**")
    sys.stdout.write(toc_lines[0]+"\n")
    fobj = open(fname, 'r')
    a_line = fobj.readline()
    while 0 != len(a_line):
        save_lines.append(a_line)
        a_line = a_line.rstrip()
        # if false_if_preproc(a_line):
        if 0 == a_line.find(toc_lines[0][0:-1]):
            line_end = save_lines[-1][len(a_line)-len(save_lines[-1])]
            found_toc = len(save_lines)-1
        re_match = re_ptrn.match(a_line)
        if re_match:
            re_end = re_match.span()[1]-1
            a_line = a_line[re_end:].lstrip()
            a_unmod = a_line
            a_line = a_line.lower()
            a_line = a_line.replace("-", r"\-")
            a_line = a_line.replace(" ", "-")
            pre_line = ""
            if found_top:
                re_end = max(2,re_end)
                for i in range(re_end-2): # one less to match top
                    pre_line += "  "
            else:
                found_top = True
                a_unmod = "Top"
            toc_lines.append("%s* [%s](#%s \"%s\")" % (pre_line, a_unmod, a_line, a_unmod))
            sys.stdout.write(toc_lines[-1] +"\n")
        a_line = fobj.readline()
    fobj.close()

    if 0 != len(line_end): # if we found the TOC in the file
        fobj = open(fname, 'w')
        for i in range(found_toc):
            fobj.write("%s" % save_lines[i])
        for i in range(found_toc, len(save_lines)):
            if len(line_end) == len(save_lines[i]):
                found_toc = i
                break
        # print("%d: %s" % (found_toc, save_lines[found_toc]))
        for a_line in toc_lines:
            fobj.write("%s%s" % (a_line,line_end))
        for i in range(found_toc, len(save_lines)):
            fobj.write("%s" % save_lines[i])
        fobj.close()
    else:
        sys.stderr.write("\nERROR - TOC not found in %s; no file written\n\n" % fname)

    # end do_create_md_TOC()

###################################################################################
# "__main__" processing for create_md_TOC
#
# use argparse to process command line arguments
# python create_md_TOC.py -h to see what the arguments are
#
if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='create_md_TOC',
        formatter_class=argparse.RawTextHelpFormatter,
        description="reads a MarkDown (*.md) file and writes to stdout a table of contents",
        epilog="""Example:
python create_md_TOC.py REAME.md > TOC_suggestions.txt
""",
        usage='%(prog)s fname')
    my_parser.add_argument('fname',type=str,help='path to MarkDown text file')
    args = my_parser.parse_args()

    do_create_md_TOC(args.fname)