# Author: Mark Olson 2022-11-25
#
# RenameReorder - organize by date images and movies from Google Photos and other sources
#
#
# HEIC code derived from code suggestion by aleksandereiken at
#   https://stackoverflow.com/questions/54395735/how-to-work-with-heic-image-file-types-in-python
#
#   Pillow appears to be in the conda base environment
#   https://anaconda.org/anaconda/pillow
#   conda install -c anaconda pillow
#
#   There does not appear to be a way to install this through conda
#   https://pypi.org/project/pyheif/ - note: License: Apache Software License
#   $ pip3 install pillow-heif
#
#   https://anaconda.org/conda-forge/piexif
#   conda install -c conda-forge piexif
#
# alternate for movies
#
# conda install opencv -- fails
# conda install -c conda-forge opencv-python  -- fails
# conda install -c conda-forge opencv  -- fails


# using sys.stdout and sys.stderr
import sys

# reading directories, changeing date/time for files
import os
import time
import datetime

# regular expresions - your best friend!
import re

# simple parsing of command arguments
import argparse

# easy way to get EXIF data
from PIL import Image
from PIL.ExifTags import TAGS 


EXTENDED_HELP = """

RenameReorder - organize by date images and movies from Google Photos and other sources

This is extended help - if you just want to know how to run it, use --help

Sometimes Google Photos (maybe only in the past) would download files that
   had the correct date/time stamp.
Sometimes it downloads files with the date/time stamp in the filename
   ex: 20211225_000000.jpg
Sometimes it downloads picture files with metadata that has the date/time stamp
   metadata accessible via exifread
Sometimes it downloads movie files with metadata that has the date/time stamp
   metadata accessible via hachoir although timestamp is in GMT
Sometimes there is no indication of time stamp

Sometimes iPhone pictures are in heic format, sometimes they are jpg or png
   with an accompanying short movie

Generate inputs with this for PNG & JPG

echo y | rm nodate.txt
echo y | rm yesdate.txt
for v in *.jpg *.JPG *.jpeg *.JPEG *.png *.PNG
do
d=`EXIF -t DateTime ${v} | grep "DateTime " | sed "s?^.*ASCII.: ??" | sed "s?[:][0-9][0-9]\\$?:&?" | sed "s?::?.?" | sed "s?[: ]??g"`
if test -z "$d"; then  echo $v | grep -v "[*]" >> nodate.txt; else  echo "${d};${v}" >> yesdate.txt; fi
done

Generate inputs with this for MOV & MP4 & MP

for v in *.MOV *.mov *.MP *.mp *.MP4 *.mp4 *.avi *.AVI
do
d=`hachoir-metadata "$v" 2> /dev/nul | grep -i creation.date | sed "s?.*date: ??" | sed "s?[:-]??g" | sed "s? ??" | sed "s?[0-9][0-9]\\$?.&?"`
if test -z "$d"; then
  echo $v | grep -v "[*]" >> nodate.txt
  else  echo "${d};${v}" >> yesdate.txt
fi
done

Get EXIF like this (mdo environment is an example) (this for JPG & PNG)

---> from Anaconda prompt in mdo Anaconda environment:
$ pip install exifread
Collecting exifread
  Downloading ExifRead-3.0.0-py3-none-any.whl (40 kB)
      ---------------------------------------- 40.4/40.4 kB 1.9 MB/s eta 0:00:00
Installing collected packages: exifread
Successfully installed exifread-3.0.0

---> from git bash in mdo environment
$ alias EXIF="python /d/anaconda3/envs/mdo/Scripts/EXIF.py"



   ------------> note: associated MP4 files from iPhone have metadata a few secs after JPG
   ------------> also the metadata is in UTC/GMT not local time
   ------------> suggestion: use "USE_STAR_ON_TOUCH_MV = True"
   ------------>    and don't use the MP4 metadata to process JPG-associated MP4
Get hachoir-metadata like this (mdo environment is an example) (this for MOV & MP4)

---> from Anaconda prompt in mdo Anaconda environment:
$ pip install hachoir
Collecting hachoir
  Downloading hachoir-3.1.3-py3-none-any.whl (647 kB)
      -------------------------------------- 647.3/647.3 kB 4.1 MB/s eta 0:00:00
Installing collected packages: hachoir
Successfully installed hachoir-3.1.3

$ hachoir-metadata IMG_0985.MOV | grep -i creation.date
- Creation date: 2021-04-25 03:42:38
$ hachoir-metadata IMG_0985.MOV | grep -i creation.date | sed "s?.*date: ??"
2021-04-25 03:42:38
$ which hachoir-metadata
/d/anaconda3/envs/mdo/Scripts/hachoir-metadata



  read inputs from stdin in the form (should be sorted by last column)
202108141353.54;20210814_135354.jpg
202108141353.59;20210814_135359.jpg
202103051441.09;IMG_0875.JPG
202103051441.09;IMG_0876.JPG


  output to sdtout; note dup date gets _01 then _02
  this using the default USE_STAR_ON_TOUCH_MV = True # use "*" for touch and rename all movie files the same
touch --no-create -t 202101011158.51 "IMG_0772".*
mv "IMG_0772.JPG" 20210101_115851.JPG
test -f "IMG_0772.MOV" && mv "IMG_0772.MOV" 20210101_115851.MP4
test -f "IMG_0772.mov" && mv "IMG_0772.mov" 20210101_115851.MP4
test -f "IMG_0772.MP" && mv "IMG_0772.MP" 20210101_115851.MP4
test -f "IMG_0772.mp" && mv "IMG_0772.mp" 20210101_115851.MP4
test -f "IMG_0772.avi" && mv "IMG_0772.avi" 20210101_115851.MP4
test -f "IMG_0772.AVI" && mv "IMG_0772.AVI" 20210101_115851.MP4
test -f "IMG_0772.MP4" && mv "IMG_0772.MP4" 20210101_115851.MP4
test -f "IMG_0772.mp4" && mv "IMG_0772.mp4" 20210101_115851.MP4
touch --no-create -t 202101011159.08 "IMG_0773".*
mv "IMG_0773.JPG" 20210101_115908.JPG
test -f "IMG_0773.MOV" && mv "IMG_0773.MOV" 20210101_115908.MP4
test -f "IMG_0773.mov" && mv "IMG_0773.mov" 20210101_115908.MP4
test -f "IMG_0773.MP" && mv "IMG_0773.MP" 20210101_115908.MP4
test -f "IMG_0773.mp" && mv "IMG_0773.mp" 20210101_115908.MP4
test -f "IMG_0773.avi" && mv "IMG_0773.avi" 20210101_115908.MP4
test -f "IMG_0773.AVI" && mv "IMG_0773.AVI" 20210101_115908.MP4
test -f "IMG_0773.MP4" && mv "IMG_0773.MP4" 20210101_115908.MP4
test -f "IMG_0773.mp4" && mv "IMG_0773.mp4" 20210101_115908.MP4
touch --no-create -t 202103051441.09 "IMG_0875".*
mv "IMG_0875.JPG" 20210305_144109.JPG
test -f "IMG_0875.MOV" && mv "IMG_0875.MOV" 20210305_144109.MP4
test -f "IMG_0875.mov" && mv "IMG_0875.mov" 20210305_144109.MP4
test -f "IMG_0875.MP" && mv "IMG_0875.MP" 20210305_144109.MP4
test -f "IMG_0875.mp" && mv "IMG_0875.mp" 20210305_144109.MP4
test -f "IMG_0875.avi" && mv "IMG_0875.avi" 20210305_144109.MP4
test -f "IMG_0875.AVI" && mv "IMG_0875.AVI" 20210305_144109.MP4
test -f "IMG_0875.MP4" && mv "IMG_0875.MP4" 20210305_144109.MP4
test -f "IMG_0875.mp4" && mv "IMG_0875.mp4" 20210305_144109.MP4
touch --no-create -t 202103051441.09 "IMG_0876".*
mv "IMG_0876.JPG" 20210305_144109_01.JPG
test -f "IMG_0876.MOV" && mv "IMG_0876.MOV" 20210305_144109_01.MP4
test -f "IMG_0876.mov" && mv "IMG_0876.mov" 20210305_144109_01.MP4
test -f "IMG_0876.MP" && mv "IMG_0876.MP" 20210305_144109_01.MP4
test -f "IMG_0876.mp" && mv "IMG_0876.mp" 20210305_144109_01.MP4
test -f "IMG_0876.avi" && mv "IMG_0876.avi" 20210305_144109_01.MP4
test -f "IMG_0876.AVI" && mv "IMG_0876.AVI" 20210305_144109_01.MP4
test -f "IMG_0876.MP4" && mv "IMG_0876.MP4" 20210305_144109_01.MP4
test -f "IMG_0876.mp4" && mv "IMG_0876.mp4" 20210305_144109_01.MP4

"""

# flag to use "*" on touch
USE_STAR_ON_TOUCH_MV = True # use "*" for touch and rename all movie files the same

# all files will be either *.JPG or *.MP4
#    *.jpg or *.mp4 will just be renamed
#    if they are these others then we will make a copy of them, saving the renamed file
COPY_EXTENSIONS = { "MOV": "MP4", "mov": "MP4", "MP": "MP4", "mp": "MP4", "avi": "MP4", "AVI": "MP4", "jpeg": "JPG", "JPEG": "JPG", "png": "JPG", "PNG": "JPG" }
# note: this one includes MP4 because it is all extensions that might be associated with an iPhone image
MP4_EXTENSIONS = { "MOV": "MP4", "mov": "MP4", "MP": "MP4", "mp": "MP4", "avi": "MP4", "AVI": "MP4", "MP4": "MP4", "mp4": "MP4" }
# note: this includes all non-HEIC picture extensions
PIX_EXTENSIONS = { "jpg": "JPG", "JPG": "JPG", "jpeg": "JPG", "JPEG": "JPG", "png": "JPG", "PNG": "JPG" }

###################################################################################
# get_exif_date_str - get exif date/time string (ex: '2021:12:24 21:02:51')
#
# returns None if no exif date/time string
#
def get_exif_date_str(fname):
    my_image= open(fname, 'rb')

    image = Image.open(my_image)
    image.verify()
    exif =  image._getexif()

    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    my_image.close()

    orgDate = None
    if "DateTimeOriginal" in labeled.keys():
        orgDate = labeled["DateTimeOriginal"]
    return orgDate
    # end get_exif_date_str()

###################################################################################
# my_touch - change file access and modified time
#
# fname is the filename
# stamp is of the form CCYYMMDDhhmm.ss  (similar to touch -t STAMP)
#   example for 2021-12-24 11:59:58, stamp would be
#      "202112241159.58"
#
# COMMON WINDOWS TIME REPRESENTATIONS
# When browsing folders, Windows Explorer won't display dates outside a specific range:
#   The MS-DOS date format can represent only dates between 1/1/1980 and 12/31/2107.
# When NTFS didn't exist, the created, modified, and access dates were designed to take 16 bits each (2 bytes).
# The information gets packed like this:
#   Bits | Description
#   -------------------------------------------------------
#   0–4  | Day (1-31)
#   5–8  | Month (1 = January, 2 = February, etc.)
#   9-15 | Year offset from 1980 (0 = 1980, 1 = 1981, etc.)
# the year offset is 1980; 0x00 above is 1980, 0x127 above is 2107
# The FAT file system stores time values based on the local time of the computer.
# 
# For NTFS a file time is a 64-bit value that represents the number of
#   100-nanosecond intervals that have elapsed since 12:00 A.M. January 1, 1601
#   Coordinated Universal Time (UTC).
# The NTFS file system stores time values in UTC format, so they are not
#   affected by changes in time zone or daylight saving time.
#
# COMMON LINUX/UNIX/ETC TIME REPRESENTATIONS
# The Unix time_t data type that represents a point in time is, on many platforms,
#   a signed integer, traditionally of 32 bits (but see below), directly
#   encoding the Unix time number as described in the preceding section.
# Being 32 bits means that it covers a range of about 136 years in total.
# The minimum representable date is Friday 1901-12-13, and the maximum
#   representable date is Tuesday 2038-01-19.
# One second after 03:14:07 UTC 2038-01-19 this representation will overflow
#   in what is known as the year 2038 problem.
# In some newer operating systems, time_t has been widened to 64 bits.
#   This expands the times representable by approximately 292 billion years
#   in both directions, which is over twenty times the present age of the
#   universe per direction.
# There was originally some controversy over whether the Unix time_t should be
#   signed or unsigned. If unsigned, its range in the future would be doubled,
#   postponing the 32-bit overflow (by 68 years). However, it would then be
#   incapable of representing times prior to the epoch.
# The consensus is for time_t to be signed, and this is the usual practice.
# The software development platform for version 6 of the QNX operating system
#   has an unsigned 32-bit time_t, though older releases used a signed type.
#
def my_touch(fname, stamp):
    req_stamp = "^[12][0-9]{3}[01][0-9][0-3][0-9][0-5][0-9][0-5][0-9][.][0-5][0-9]$"
    if not re.search(req_stamp, stamp):
        sys.stderr("ERROR: my_touch() bad timestamp f=|%s| s=|%s|\n" % (fname, stamp))
        return
    a_year = stamp[:4]
    a_month = stamp[4:6]
    a_day = stamp[6:8]
    a_hour = stamp[8:10]
    a_minute = stamp[10:12]
    a_second = stamp[-2:]
    
    a_date = datetime.datetime(year=a_year, month=a_month, day=a_day, hour=a_hour, minute=a_minute, second=a_second)
    a_changeTime = time.mktime(a_date.timetuple())
    
    os.utime(fname, (a_changeTime, a_changeTime)) # access time, modified time
    # end my_touch

###################################################################################
# do_rename_reorder - create the *.sh to do rename and reorder
#
# read the sorted-by-date lines in format
#     202103051441.09;IMG_0875.JPG
#
def do_rename_reorder(the_lines):
    # these variables are for handling different-name files with same date
    prev_date = ""
    prev_filename_only = ""
    num_date_match = 0
    
    for a_line in the_lines:
        a_line = a_line.strip()
        
        # check if we should process this line
        semicolon = a_line.find(";")
        if (0 != len(a_line)) and (semicolon == 15):
            inp_date = a_line[:semicolon]
            inp_fname = a_line[semicolon+1:]
            inp_fname_only = inp_fname[:inp_fname.rfind(".")]
            # print("\n\nDEBUG %s" % (a_line))
            # print("DEBUG --  %d |%s| |%s|\n\n" % (semicolon, inp_fname, inp_date))
            tmp_date = inp_date.replace(".", "")
            if (prev_date == tmp_date) and (prev_filename_only != inp_fname_only):
                prev_filename_only = inp_fname_only
                num_date_match += 1
                tmp_date += "_%02d" % num_date_match
            else:
                prev_date = tmp_date
                prev_filename_only = inp_fname_only
                num_date_match = 0
            
            # now touch the file - either with a "*" extension or the original file name
            if USE_STAR_ON_TOUCH_MV:
                sys.stdout.write("touch --no-create -t %s \"%s\".*\n" % (inp_date, inp_fname_only))
            else:
                sys.stdout.write("touch --no-create -t %s \"%s\"\n" % (inp_date, inp_fname))
            
            
            # rename old file to new filename with upper case of its existing extension
            inp_ext = inp_fname.split(".")[-1]
            otp_ext = inp_ext.upper()
            otp_fname_only = tmp_date[:8] + "_" + tmp_date[8:] + "."
            otp_fname = otp_fname_only + otp_ext
            sys.stdout.write("mv \"%s\" %s\n" % (inp_fname, otp_fname))
            
            # if the file has an extension other than (either upper/lower case)
            #    JPG - copy to *.JPG in upper case
            #    MP4  - copy to *.MP4 in upper case
            if inp_ext in COPY_EXTENSIONS:
                sys.stdout.write("cp -p \"%s\" %s\n" % (otp_fname, otp_fname_only+COPY_EXTENSIONS[inp_ext]))
                
            if USE_STAR_ON_TOUCH_MV:
                # if there is an associated movie file (already touch'ed), move to same name
                # these days the browsers can handle it if the extension is wrong but close
                for ext in MP4_EXTENSIONS.keys():
                    sys.stdout.write("test -f \"%s.%s\" && mv \"%s.%s\" %sMP4\n" % (inp_fname_only, ext, inp_fname_only, ext, otp_fname_only))
                pass
            
            # now all files will have a version either *.JPG or *.MP4
    
        # here if the line should not be processed
        else:
            sys.stderr.write("\nERROR: bad line |%s|\n\n" % a_line)
    
        a_line = sys.stdin.readline()
    # end do_rename_reorder()

###################################################################################
# get_the_lines - read directory, create sorted lines for do_rename_reorder
#
def get_the_lines(dir_of_interest):
    # generate regular expressions for movie and picture filenames
    re_mp4 = ""
    for mp4_ext in MP4_EXTENSIONS.keys():
        re_mp4 += "\." + mp4_ext + "$|"
    re_mp4 = re_mp4[:-1] # we know there is at least one
    re_pix = ""
    for pix_ext in PIX_EXTENSIONS.keys():
        re_pix += "\." + pix_ext + "$|"
    re_pix = re_pix[:-1] # we know there is at least one
    re_mp4 = re.compile(re_mp4)
    re_pix = re.compile(re_pix)
    re_heic = re.compile("\.HEIC$|\.heic$")


    # first collect the non-HEIC filenames
    # we want sorted by filename so any associated *.MP4 etc. files are near
    filenames_all = sorted(os.listdir(dir_of_interest))
    
    # filenums_pix_etc has [["file_only", {idx_pix: "idx"]]
    filenums_pix_etc = []
    for idx, filename in enumerate(filenames_all):
        if not (re_mp4.search(filename) or re_pix.search(filename)):
            continue
        idot = filename.rfind(".")
        idx_pix = -1
        if re_pix.search(filename):
            idx_pix = idx
        if (0 == len(filenums_pix_etc)) or (filename[:idot] != filenums_pix_etc[-1][0]):
            filenums_pix_etc.append([filename[:idot], {idx_pix: "idx"}])
        else:
            filenums_pix_etc[-1][1][idx] = "idx"

    # collect HEIC files
    filenumsHEIC = []
    for idx, filename in enumerate(filenames_all):
        if re_heic.search(filename):
            filenumsHEIC.append(idx)

    # TODO FIXME now get the dates from the metadata
    # set all associated pix files to same date
    # end get_the_lines()

###################################################################################
# "__main__" processing for RenameReorder
#
# use argparse to process command line arguments
# python RenameReorder.py -h to see what the arguments are
#
if __name__ == "__main__":

    my_parser = argparse.ArgumentParser(prog='RenameReorder',
        formatter_class=argparse.RawTextHelpFormatter,
        description="organize by date images and movies from Google Photos and other sources\n" +
        "reads data from stdin; --helphelp shows format\n" +
        "stdout receives bash shell script to set filedates and filename\n",
        epilog="""Example:
python RenameReorder.py < inpfile  > rename_reorder.sh
""",
        usage='%(prog)s listFname < inpfile > outfile.sh')
    # my_parser.add_argument('listFname',type=str,help='path to listFname text file, copied from Kindle book list')
    my_parser.add_argument('-hh',
                           '--helphelp',
                           action='store_true',
                           help='show extended help message')
    me_group1 = my_parser.add_mutually_exclusive_group(required=False)
    me_group1.add_argument('-gtp',
                           '--gentext_pixonly',
                           action='store_true',
                           help='generate text file for date;pixonly')
    me_group1.add_argument('-gtm',
                           '--gentext_movonly',
                           action='store_true',
                           help='generate text file for date;movonly')
    me_group1.add_argument('-gtb',
                           '--gentext_pix_mov',
                           action='store_true',
                           help='generate text file for date;pix_or_mov')
    args = my_parser.parse_args()
    
    if args.helphelp:
        sys.stdout.write("%s" % EXTENDED_HELP)
    else:
        inp_lines = sys.stdin.readlines() # read all the input from stdin
        the_lines = sorted(inp_lines) # sort by date then by filename
        del inp_lines
        do_rename_reorder(the_lines)
