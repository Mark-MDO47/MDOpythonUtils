# Process Photos - sort Google Photos downloads by date/time

## RenameReorder.py

Originally written to handle rename and touch of files to reflect date/time in photo or movie metadata gathered using bash scripts.
Now I am adding code to allow it to do the entire job
* Pro - less manual steps, more tailored approach due to knowledge of all files and filenames
* Con - cannot manually modify intermediate files to get desired results

I take the Google Photos from one Apple iPhone and one Pixel and try to combine them and index them.

I did finally get the iPhone set up to not create *.HEIC files. Now it creates a picture and a short movie, with the same filename but different extensions.
There are probably some further things that could be configured in the phones to make this process easier, but I have years of photos and movies to process.

When downloaded, the files have a name such as IMG_####.JPG and the file has today's date/time not the time of the photo. Fortunately there is some metadata (EXIF) that has the date the photo was taken.
- first read all the picture files (.JPG, .PNG, etc.) and the metadata
- using the date/time from the metadata, set the file date and rename the file(s) (picture file and any associated movie file) to the date/time in sortable order
- for the picture files that don't have a date/time; keep a list of them
- for movie files that are not associated with picture files, read the metadata and do the same rename etc. as above
- for the movie files that don't have a date/time; keep a list of them
