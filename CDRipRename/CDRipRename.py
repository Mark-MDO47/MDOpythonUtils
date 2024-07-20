# -*- coding: utf-8 -*-
"""
usage: CDRipRename dirname other

renames CD RIP fnames to longer names based on trackname file

positional arguments:
  textfile              path to text file with names

options:
  -h, --help            show this help message and exit
  -nd NUMDIGITS, --numdigits NUMDIGITS
                        optional num digits for output filename; default 2
  -s STARTWITH, --startwith STARTWITH
                        optional string required at start of input file name

Example:
python CDRipRename.py "D:\path-to-my\SoundForgeTextFile.txt" > rename_cmds.sh

NOTE: directory containing SoundForgeTextFile also contains RIP files
    example: CD_01.wav, CD_01.mp3, CD_02.wav, etc.
    this might generate
        mv CD_01.wav CD_01_F_Chopin_Ballade_in_F_major_Op38_Bruce_Xiaoyu_Liu.wav
        mv CD_02.mp3 CD_02_F_Chopin_Rondo_a_la_Mazur_in_F_major_Op5_Bruce_Xiaoyu_Liu.mp3
        mv CD_02.wav CD_02_F_Chopin_Rondo_a_la_Mazur_in_F_major_Op5_Bruce_Xiaoyu_Liu.wav

    Of course you can use sed or other means to re-arrange and/or shorten the strings:
python CDRipRename.py -s CD -nd 3 SoundForgeTextFile.txt | sed "s?F_Chopin?Chopin?"

@author: https://github.com/Mark-MDO47
"""

import os
import sys
# import copy
import argparse

COLUMNS_USED = {"title": "Title", "name": "Name", "artist": "Artist"}
COLUMN_NUMS =  {"title": -1, "name": -1, "artist": -1}
FILE_EXTS = [".wav", ".mp3"]

###################################################################################
# print_rename - print rename commands
def print_rename(a_num_str, starts_with, use_leading_tracnum, trac_name, artist_name, filenames, fout):
    trac_name_win_fname = trac_name.replace(" ","_").replace(".","").replace("(","").replace(")","").replace("'","").replace("[","").replace("]","").replace(",","")
    if (not use_leading_tracnum) and trac_name_win_fname[0].isdigit():
        while trac_name_win_fname[0].isdigit():
            trac_name_win_fname = trac_name_win_fname[1:]
        while "_" == trac_name_win_fname[0]:
            trac_name_win_fname = trac_name_win_fname[1:]
    artist_name_win_fname = artist_name.replace(" ","_").replace(".","").replace("(","").replace(")","").replace("'","").replace("[","").replace("]","").replace(",","")
    for a_fn in filenames:
        if (0 != len(starts_with)) and (0 != a_fn.find(starts_with)):
            continue
        tmp_dot = a_fn.rfind(".")
        if -1 == tmp_dot:
            continue
        a_fn_ext = a_fn[tmp_dot:]
        if a_fn_ext not in FILE_EXTS:
            continue
        tmp_underscore = a_fn.rfind("_")
        if -1 == tmp_underscore:
            continue
        a_fn_num = -1 # keep in scope
        try:
            a_fn_num = int(a_fn[1+tmp_underscore:tmp_dot])
        except:
            a_fn_num = -1
        if -1 == a_fn_num:
            continue
        if a_fn_num == int(a_num_str,10):
            # fout.write("mv %s %s_%s_%s%s\n" % (a_fn, a_fn[:tmp_underscore],a_num_str,trac_name_win_fname,a_fn_ext))
            fout.write("mv %s %s_%s_%s%s%s\n" % (a_fn, a_fn[:tmp_underscore],a_num_str,trac_name_win_fname,artist_name_win_fname,a_fn_ext))
    # end print_rename()

###################################################################################
# process_column_line - process the text file
def process_column_line(col_names, a_line, line_num, fname, fout, ferr):
    found_all_cols = True
    for a_col in COLUMNS_USED:
        if COLUMNS_USED[a_col] not in col_names:
            found_all_cols = False
            ferr.write("ERROR - column |%s| not found line %d file %s\n" % (a_col, line_num, fname))
        else:
            COLUMN_NUMS[a_col] = col_names.index(COLUMNS_USED[a_col])
    return found_all_cols
    # end process_column_line()

###################################################################################
# do_CDRipRename - process the text file
def do_CDRipRename(fname, numdigits, starts_with, use_leading_tracnum, fout, ferr):

    # this will give error message if file not present
    finp = open(fname,'rt')

    # format string for file number
    fmt_str = "%0" + "%d" % numdigits + "d"

    # get list of filenames in directory containing text file
    fn_path = os.path.dirname(os.path.abspath(fname))
    filenames = sorted(os.listdir(fn_path))

    found_title_line = False
    # my old-fashioned method to read fname (a text file) line by line
    line_num = 0
    a_line = finp.readline()
    while 0 != len(a_line):
        line_num += 1
        a_line = a_line.strip()
        a_split = a_line.split("\t")
        if found_title_line and a_line[0].isdigit():
            a_num = int(a_split[COLUMN_NUMS["title"]])
            trac_name = a_split[COLUMN_NUMS["name"]].strip()
            artist_name = ""
            if len(a_split) > COLUMN_NUMS["artist"]:
                artist_name = "_" + a_split[COLUMN_NUMS["artist"]].strip()
            print_rename(fmt_str % a_num, starts_with,use_leading_tracnum, trac_name, artist_name, filenames, fout)
        elif a_split[0] == COLUMNS_USED["title"]:
            col_names = []
            for tmp_col in a_split: # remove entries for extra tabs
                if len(tmp_col):
                    col_names.append(tmp_col)
            if not process_column_line(col_names, a_line, line_num, fname, fout, ferr):
                ferr.write("ABORTING...\n\n")
                exit(1)
            found_title_line = True
        else:
            pass # keep looking for title line

        a_line = finp.readline()

    # end do_CDRipRename()


###################################################################################
# "__main__" processing for CDRipRename
#
# use argparse to process command line arguments
# python CDRipRename.py -h to see what the arguments are
#
if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='CDRipRename',
        formatter_class=argparse.RawTextHelpFormatter,
        description="renames CD RIP fnames to longer names based on trackname file",
        epilog="""Example:
python CDRipRename.py "%s" > rename_cmds.sh

NOTE: directory containing SoundForgeTextFile also contains RIP files
    example: CD_01.wav, CD_01.mp3, CD_02.wav, etc.
    this might generate
        mv CD_01.wav CD_01_F_Chopin_Ballade_in_F_major_Op38_Bruce_Xiaoyu_Liu.wav
        mv CD_02.mp3 CD_02_F_Chopin_Rondo_a_la_Mazur_in_F_major_Op5_Bruce_Xiaoyu_Liu.mp3
        mv CD_02.wav CD_02_F_Chopin_Rondo_a_la_Mazur_in_F_major_Op5_Bruce_Xiaoyu_Liu.wav

    Of course you can use sed or other means to re-arrange and/or shorten the strings:
python CDRipRename.py -s CD -nd 3 SoundForgeTextFile.txt | sed \"s?F_Chopin?Chopin?\"
""" % r"D:\path-to-my\SoundForgeTextFile.txt",
        usage='%(prog)s dirname other')
    my_parser.add_argument('textfile',type=str,help='path to text file with names')
    my_parser.add_argument('-nd', '--numdigits', default='2', type=int,
                           help='optional num digits for output filename; default 2')
    my_parser.add_argument('-s', '--startwith', type=str, default="",
                           help='optional string required at start of input file name')
    my_parser.add_argument('-u', '--use_leading_tracnum', action='store_true',
                           help='don\'t remove duplicate leading trac num')
    # my_parser.add_argument('-v', '--verbose', action='store_true',
    #                        help='print verbose information about starting conditions')

    args = my_parser.parse_args()

    do_CDRipRename(args.textfile,args.numdigits,args.startwith,args.use_leading_tracnum,sys.stdout,sys.stderr)
