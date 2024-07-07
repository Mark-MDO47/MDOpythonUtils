# -*- coding: utf-8 -*-
"""
DirectoryWalk - traverses and compares two directory trees
   (Windows only at this time)

usage: DirectoryWalk dirname other

Traverses parallel directories, flagging differences

positional arguments:
  dirname             path to root directory to compare
  other               Drive letter to other directory to compare

options:
  -h, --help          show this help message and exit

mutually exclusive options:
  -ci, --ignore       do not compare files found in both directories (just flag missing files)
  -cs, --sha256       compare files found in both directories using SHA256; default is SHA256 comparison
  -cl, --length_date  FUTURE-FEATURE compare files found in both directories using file-length and modify-date-time

Example:
python DirectoryWalk.py "D:\path-to-my\StuffAndInterests" X > DirectoryCompareInfo.txt

@author: https://github.com/Mark-MDO47

"""

import os
import sys
import hashlib
import argparse

GBL_COMPARE_TYPE = "SHA256" # default

TEST_D = r"D:\OlsonMedia\StuffAndInterests\BooksPapers\KindleMark"
TEST_X = r"X:\OlsonMedia\StuffAndInterests\BooksPapers\KindleMark"
DEFAULT_D = r"D:\OlsonMedia\StuffAndInterests"
DEFAULT_X = r"X:\OlsonMedia\StuffAndInterests"

# these to not process certain directories/files
# regular expressions are just too tweaky
Trunc_Dirs_Calc = {r':\OlsonMedia\StuffAndInterests\Quant': 1}
Skip_Dirs = {"AtEnd": [".AppleDouble", ".git", ".svn"], "AtStart": [], "All": []}
Skip_Dirs_Len = {"AtEnd": [], "AtStart": [], "All": []}
Skip_Files = {"AtEnd": [".bak", ".ipynb", ".lnk"], "AtStart": ["~"], "All": ["Thumbs.db", ".DS_Store"]}
Skip_Files_Len = {"AtEnd": [], "AtStart": [], "All": []}

# only calculate lengths one time
for gbl_a_key in Skip_Dirs.keys():
    gbl_a_list = Skip_Dirs[gbl_a_key]
    for an_entry in gbl_a_list:
        Skip_Dirs_Len[gbl_a_key].append(len(an_entry))
for gbl_a_key in Skip_Files.keys():
    gbl_a_list = Skip_Files[gbl_a_key]
    for an_entry in gbl_a_list:
        Skip_Files_Len[gbl_a_key].append(len(an_entry))


# List to store all directories files
L_idx_root = 0
L_idx_dirs = 1
L_idx_files = 2
L_d = []
L_x = []
# Dictionary so can check existence using hash
Dir_d = {}
Dir_x = {}

###################################################################################
# do_sha256 - compute string sha_256 of a file
#    returns: string
def do_sha256(fn):
    sha256_str = "UNKNOWN"
    try:
        sha256_1 = hashlib.sha256()
        with open(fn,'rb') as fptr:
            sha256_1.update(fptr.read())
        sha256_str = sha256_1.hexdigest()
    except:
        sys.stderr.write("ERROR SHA256 %s\n" % fn)
    # if fptr:
    #     fptr.close()
    # if sha256_1:
    #     del sha256_1
    return sha256_str
    # end do_sha256()

###################################################################################
# MatchName - match a name to params
#   if the name matches any of the params, return True. Else return False.
def MatchName(name_to_check, skip_list, skip_list_len):
    the_match = False
    for a_key in skip_list.keys():
        for idx, a_match_str in enumerate(skip_list[a_key]):
            if "AtEnd" == a_key:
                if a_match_str == name_to_check[-skip_list_len[a_key][idx]:]:
                    the_match = True
                    break
            elif "AtStart" == a_key:
                if a_match_str == name_to_check[:skip_list_len[a_key][idx]]:
                    the_match = True
                    break
            elif "All" == a_key:
                if a_match_str == name_to_check:
                    the_match = True
                    break
            else:
                sys.stderr.write("ERROR MatchName found illegal key %s\n" % a_key)
                sys.exit(1)
        if True == the_match:
            break
    return the_match
    # end MatchName()

###################################################################################
# TrimNames - trim skip_names from list
#    returns a list of files that do not match the file criteria
def TrimNames(inp_name_list, skip_names, skip_names_len):
    otp_name_list = []
    for a_file in inp_name_list:
        if not MatchName(a_file, skip_names, skip_names_len):
            otp_name_list.append(a_file)
    return otp_name_list
    # end TrimNames()

###################################################################################
# SkipDirs - match final dir name
#   if the name matches any of the params, return True. Else return False.
def SkipDirs(dir_name):
    only_dir_name = dir_name
    if "\\" in dir_name:
        only_dir_name = dir_name[1+dir_name.rfind("\\"):]
    return MatchName(only_dir_name, Skip_Dirs, Skip_Dirs_Len)
    # end SkipDirs()

###################################################################################
# FindNotIn - find root directories in one dict not in another
def FindNotIn(dir_1, dir_2):
    dir_not_in = []
    root_dir_not_in = "UNKNOWNUNKNOWN"
    for a_dir in dir_1:
        if a_dir not in dir_2:
            if -1 == a_dir.find(root_dir_not_in):
                dir_not_in.append(a_dir)
                root_dir_not_in = a_dir
    return dir_not_in
    # end FindNotIn()


###################################################################################
# Print_With_Title - if need to print title, first print that then string
def Print_With_Title(title_string, string_to_print):
    if title_string:
        print("\n%s" % title_string)
        title_string = False
    print("%s" % string_to_print)
    return title_string
    # end Print_With_Title()

###################################################################################
# CompareFileLists_OneSided - compare list checking all files in files_1
def CompareFileLists_OneSided(do_compare, root, char_1, char_2, files_1, files_2):
    title_string = "***** FILES %s or %s %s" % (char_1, char_2, root)
    for a_file_1 in files_1:
        if a_file_1 in files_2:
            # file in both sides - compare files
            if "SHA256" == do_compare:
                sha256_str1 = do_sha256(char_1+root+"\\"+a_file_1)
                sha256_str2 = do_sha256(char_2+root+"\\"+a_file_1)
                if ("UNKNOWN" != sha256_str1) and ("UNKNOWN" != sha256_str2):
                    # normal case - SHA256 worked
                    if sha256_str1 != sha256_str2:
                        title_string = Print_With_Title(title_string, "  %s: %s SHA256 does not match %s:" % (char_1, a_file_1, char_2))
                else:
                    # SHA256 error - maybe one of the drives got unmounted due to WiFi?
                    if "UNKNOWN" == sha256_str1:
                        title_string = Print_With_Title(title_string, "  SHA ERROR calculating SHA256 on %s %s" % (char_1, a_file_1))
                    if "UNKNOWN" == sha256_str2:
                        title_string = Print_With_Title(title_string, "  SHA ERROR calculating SHA256 on %s %s" % (char_2, a_file_1))
            elif "LENGTH_DATE" == do_compare:
                f_mtime1 = os.path.getmtime(char_1+root+"\\"+a_file_1)
                f_mtime2 = os.path.getmtime(char_2+root+"\\"+a_file_1)
                numbytes1 = os.path.getsize(char_1+root+"\\"+a_file_1)
                numbytes2 = os.path.getsize(char_2+root+"\\"+a_file_1)
                if (f_mtime1 != f_mtime2) or (numbytes1 != numbytes2):
                    timing_1_comparedto_2 = "same"
                    if f_mtime1 > f_mtime2:
                        timing_1_comparedto_2 = "later"
                    elif f_mtime1 < f_mtime2:
                        timing_1_comparedto_2 = "earlier"
                    sizing_1_comparedto_2 = "same"
                    if numbytes1 > numbytes2:
                        sizing_1_comparedto_2 = "larger"
                    elif numbytes1 < numbytes2:
                        sizing_1_comparedto_2 = "smaller"
                    title_string = Print_With_Title(title_string, \
                         " %s: %s datetime/length does not match %s: %s: datetime is %s and numbytes is %s as %s:" \
                         % (char_1, a_file_1, char_2, char_1, timing_1_comparedto_2, sizing_1_comparedto_2, char_2))
            elif "IGNORE" == do_compare:
                pass # Second call; don't do calculation two times
            else:
                sys.stderr.write("CompareFile do_compare not SHA not LEN_DATE but %s\n" % do_compare)
                return
        else:
            # file in side 1 but not 2
            title_string = Print_With_Title(title_string, "  file %s %s not in %s" % (char_1, a_file_1, char_2))
    # end CompareFileLists_OneSided()

###################################################################################
# CompareFileLists - compare list checking all files in both lists
def CompareFileLists(compare_type, root, char_1, char_2, files_1, files_2):
    CompareFileLists_OneSided(compare_type, root, char_1, char_2, files_1, files_2)
    # above already does requested compare of files found in both directories
    #   don't waste time by doing it again
    CompareFileLists_OneSided("IGNORE", root, char_2, char_1, files_2, files_1)
    # end CompareFileLists()


###################################################################################
# TraverseDirs return list and dict for traverse directories
#    Limitation: Windows only
# directory paths do not include the drive letter
def TraverseDirs(full_path_start_dir):
    L = []
    Dir = {}
    i = 0
    for root, dirs, files in os.walk(full_path_start_dir):
        truncate = False
        for a_trunc in Trunc_Dirs_Calc:
            if -1 != root.find(a_trunc):
                truncate = True
                break
        if SkipDirs(root):
            Trunc_Dirs_Calc[root[1:]] = 1
            truncate = True
        elif not truncate:
            files = TrimNames(files, Skip_Files, Skip_Files_Len)
            # Adding the directory info to list
            L.append((root[1:], dirs, files))
            Dir[root[1:]] = i
            i += 1
    return L, Dir
    # end TraverseDirs()

###################################################################################
# "__main__" processing for DirectoryWalk
#
# use argparse to process command line arguments
# python DirectoryWalk.py -h to see what the arguments are
#
if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='DirectoryWalk',
        formatter_class=argparse.RawTextHelpFormatter,
        description="Traverses parallel directories, flagging differences",
        epilog="""Example:
python DirectoryWalk.py "%s" X > DirectoryCompareInfo.txt
""" % r"D:\path-to-my\StuffAndInterests",
        usage='%(prog)s dirname other')
    my_parser.add_argument('dirname',type=str,help='path to root directory to compare')
    my_parser.add_argument('other',type=str,help='Drive letter to other directory to compare')
    my_parser.add_argument('-v',
                           '--verbose',
                           action='store_true',
                           help='print verbose information about starting conditions)')
    me_group = my_parser.add_mutually_exclusive_group(required=False)
    me_group.add_argument('-ci',
                           '--cmp_ignore',
                           action='store_true',
                           help='do not compare files found in both directories (just flag missing files)')
    me_group.add_argument('-cs',
                           '--cmp_sha256',
                           action='store_true',
                           help='compare files found in both directories using SHA256; default is SHA256 comparison')
    me_group.add_argument('-cl',
                           '--cmp_length_date',
                           action='store_true',
                           help='FUTURE-FEATURE compare files found in both directories using file-length and modify-date-time')

    args = my_parser.parse_args()

    if (len(args.dirname) < 3) or (not args.dirname[0].isalpha) or (":" != args.dirname[1]):
        sys.stderr.write("ERROR dirname should start with drive letter and : not %s\n" % args.dirname[:2])
        sys.exit(1)
    drive_letter_d = args.dirname[:1]
    drive_letter_x = args.other[:1]
    dirname_no_letter = args.dirname[1:]

    GBL_COMPARE_TYPE = "SHA256" # default
    if args.cmp_length_date:
        GBL_COMPARE_TYPE = "LENGTH_DATE"
    elif args.cmp_ignore:
        GBL_COMPARE_TYPE = "IGNORE"

    if args.verbose:
        print("Verbose print of DirectoryWalk starting conditions:")
        print("   dirname=\"%s\" other=\"%s\"" % (args.dirname, args.other[:1]))
        print("   file compare type = \"%s\"" % GBL_COMPARE_TYPE)


    print("\ngetting info about D: and X: directories")
    # Get info by traversing through D:
    L_d, Dir_d = TraverseDirs(drive_letter_d+dirname_no_letter)

    # Get info by traversing through X:
    L_x, Dir_x = TraverseDirs(drive_letter_x+dirname_no_letter)

    print("\nchecking for directories that exist in one but not the other...")
    # find (root) directories not in the other
    Dir_not_in_x = FindNotIn(Dir_d, Dir_x)
    Dir_not_in_d = FindNotIn(Dir_x, Dir_d)

    need_print_x = "  Not in %s:\t$$$$$$$$$$$$$$$" % drive_letter_x
    for gbl_a_dir in Dir_not_in_x:
        need_print_x = Print_With_Title(need_print_x, "    not in %s:\t%s%s" % (drive_letter_x, drive_letter_x, gbl_a_dir))
    need_print_d = "  Not in %s:\t$$$$$$$$$$$$$$$" % drive_letter_d
    for gbl_a_dir in Dir_not_in_d:
        need_print_d = Print_With_Title(need_print_d, "    not in %s:\t%s%s" % (drive_letter_d, drive_letter_d, gbl_a_dir))
    if not (need_print_x or need_print_d):
        print("   All directories found in both D: and X:")

    print("\nchecking files from matching directories")
    sorted_d_keys = sorted(Dir_d.keys())
    sorted_x_keys = sorted(Dir_x.keys())

    for gbl_idx, gbl_a_dir  in enumerate(sorted_x_keys):
        if gbl_a_dir in Dir_x:
            tuple_d = L_d[Dir_d[gbl_a_dir]]
            tuple_x = L_x[Dir_x[gbl_a_dir]]
            CompareFileLists(GBL_COMPARE_TYPE, gbl_a_dir, "D", "X", tuple_d[L_idx_files], tuple_x[L_idx_files])
        if 1 == (gbl_idx % 500):
            print("%d of %d matching directories with files checked" % (gbl_idx, len(sorted_x_keys)))

    print("Done")
