# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 19:56:57 2022
@author: mdo

HEIC code derived from code suggestion by aleksandereiken at
   https://stackoverflow.com/questions/54395735/how-to-work-with-heic-image-file-types-in-python


https://pypi.org/project/pyheif/
There does not appear to be a way to install this through conda


NEEDED - one way to install
$ pip3 install pillow-heif
$ pip3 install piexif -- this one can be done in conda; see below


Pillow appears to be in the conda base environment
https://anaconda.org/anaconda/pillow
conda install -c anaconda pillow

https://anaconda.org/conda-forge/piexif
conda install -c conda-forge piexif


"""

import os
from PIL import Image, ExifTags
from pillow_heif import register_heif_opener
from datetime import datetime
import piexif
import re
import argparse


register_heif_opener()


def convert_heic_to_jpeg(dir_of_interest):
        filenames = os.listdir(dir_of_interest)
        filenames_matched = [re.search("\.HEIC$|\.heic$", filename) for filename in filenames]

        # Extract files of interest
        HEIC_files = []
        for index, filename in enumerate(filenames_matched):
                if filename:
                        HEIC_files.append(filenames[index])

        # Convert files to jpg while keeping the timestamp
        for filename in HEIC_files:
                image = Image.open(dir_of_interest + "/" + filename)
                image_exif = image.getexif()
                if image_exif:
                        # Make a map with tag names and grab the datetime
                        exif = { ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes }
                        date = datetime.strptime(exif['DateTime'], '%Y:%m:%d %H:%M:%S')

                        # Load exif data via piexif
                        exif_dict = piexif.load(image.info["exif"])

                        # Update exif data with orientation and datetime
                        exif_dict["0th"][piexif.ImageIFD.DateTime] = date.strftime("%Y:%m:%d %H:%M:%S")
                        exif_dict["0th"][piexif.ImageIFD.Orientation] = 1
                        exif_bytes = piexif.dump(exif_dict)

                        # Save image as jpeg
                        image.save(dir_of_interest + "/" + os.path.splitext(filename)[0] + ".JPG", "jpeg", exif= exif_bytes)
                else:
                        print(f"Unable to get exif data for {filename}")
                        
# __main__
# "__main__" processing for convert_heic_to_jpeg
if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='convert_heic_to_jpeg',
        formatter_class=argparse.RawTextHelpFormatter,
        description="creates JPG of HEIC files in dir_of_interest, preserving metadata",
        epilog="""Example:
python convert_heic_to_jpeg.py dir_of_interest
""",
        usage='%(prog)s dir_of_interest')
    my_parser.add_argument('dir_of_interest',type=str,help='path to directory with HEIC files to convert')
    args = my_parser.parse_args()
    
    convert_heic_to_jpeg(args.dir_of_interest)
