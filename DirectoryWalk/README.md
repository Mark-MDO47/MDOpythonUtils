# DirectoryWalk

Sorry - at this time this tool only works properly for Windows. It assumes that paths will start with drive letters, and that the two directory trees to transverse are identical except for the drive letter.
- That happened to be true for the case I was initially interested in

```
$ python DirectoryWalk.py -h
usage: DirectoryWalk dirname other

Traverses parallel directories, flagging differences

positional arguments:
  dirname               path to root directory to compare
  other                 Drive letter to other directory to compare

options:
  -h, --help            show this help message and exit
  -v, --verbose         print verbose information about starting conditions
  -ci, --cmp_ignore     do not compare files found in both directories (just flag missing files)
  -cs, --cmp_sha256     compare files found in both directories using SHA256; default is SHA256 comparison
  -cl, --cmp_length_date
                        compare files found in both directories using file-length and modify-date-time

Example:
python DirectoryWalk.py "D:\path-to-my\StuffAndInterests" X > DirectoryCompareInfo.txt
```

## Why Not Use an Existing Sync Tool
I don't want the files changed "automatically". For instance, sometimes the earlier version of the file is the one I want to save, or contains some parts that I want to merge into the later file.

## Regarding Comparison Options
I expect that I will usually use --cmp_length_date. This is noticeably faster (especially on large files) than --cmp_sha256; however, it can give a false sense of security:
- For rare cases, the file length and modify date/time could be the same but the file different. Perhaps when working a project with other people.
- Also a rare case but does happen that there is "bit rot" on the disk media and the file reads either intermittently or always messed up on one of the locations.
  - This happened to me.
For this reason I will still occasionally use --cmp_sha256 to make sure the file integrity is still good.

Usage of --cmp_ignore is the fastest case - it will tell you if there are files/directories on one drive not found on the other.

**NOTE** - the --cmp_* options are for FILE comparison. The directories themselves are not checked directly; they are only checked for the information they return.
