# CDRipRename.py 

```
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
  -u, --use_leading_tracnum
                        don't remove duplicate leading trac num

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

```
