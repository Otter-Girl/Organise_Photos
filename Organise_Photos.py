"""
Run as .py file in python 3.8!

Input path will be requested upon running. Regular paths are valid. 
(e.g. C:/user/.../organise_me, ~/.../organise_me, ./.../organise_me, ../.../organise_me)

Required packages: Python 3.8, pathlib (BUILTINs), datetime(BUILTINs), os (native)
Functions included in this module: whichfiles, whichdir, makethedirs, movethefiles
"""


from pathlib import Path
import datetime
import os

p = input("Input path to the folder that requires sorting. Regular path types included (e.g. C:/user/.../organise_me, 
          '~/.../organise_me, ./.../organise_me, ../.../organise_me)")
datelist = whichfiles(p)
makethedirs(p, datelist)
movethefiles(p, datelist)

def whichfiles(p, filetype='image'):
    """
    Takes the user input path and returns a dict with each unique file date (last modified) as keys and matching files
    in a list as values.
    
    (Rounding to the nearest day, potential for customisability.
    'filetype' functionality currently unused.
    See file comments for discussion.)
    """
    
    p = Path(whichdir(p))   # Checks for invalid inputs, converts valid inputs to PathLike object.
    datelist = {}
    
    for files in p.iterdir():   # pathlib very useful here, iterdir, as the name implies, iterates over 
                                # successive objects in PathLike instances. 
        # The temporary variable 'filedate' is an essential stepping stone to making a useful list of folders to create.
        # datetime.fromtimestamp() recieves an epoch timestamp and converts the integer (exclusively) to a UTCdatetime object
        # (? not sure if the name 'UTCdatetime' here is right)
        # Without rounding one would see a unique folder for each file unless two files were created similtaneously (and
        # that isn't very useful.) Rounding value is to the -5th decimil point, or 10E04 seconds. For practical purposes 
        # this translates to days.
        # stat().st_mtime returns the epoch timestamp for the target.
        filedate = datetime.datetime.fromtimestamp(
                                                   int(
                                                       round(
                                                             files.stat().st_mtime
                                                             , -5
                                                             )
                                                      )
                                                   )
        # Developer thought: is the rounding pointless because we simply extract the attributes we care about in the next line?
        # Hmmm...
        year, month, day = str(filedate.year), str(filedate.month), str(filedate.day)   # Folder names are exclusively strings.
        key = '-'.join([year, month, day])          # Finally, a usable string we can use to make folders!
        datelist.setdefault(key, []).append(files)  # New keys are added as neeed due to setdefault.
                                                    # Update the relevant key with target file.
    
    return datelist


def whichdir(p, filetype='image'):
    """
    Checks if an input is really a path on the user's machine. Will prompt for a new input if it is not.
    
    N.B. Simply type 'exit' to exit the while loop if problems occur.
    
    ('filetype' functionality currently unused.)
    """
    while True:
        if not Path.is_dir(Path(p)): p = input('Please input a valid path. Again, regular path types included 
                                               '(e.g. C:/user/.../organise_me, ~/.../organise_me, ./.../organise_me, 
                                               '../.../organise_me) Alternatively, to leave type "exit" ')
        if p == 'exit': exit()
    return p


def makethedirs(p, datelist):
    """
    Makes a folder for each key in datelist in the target path.
    """
    # Developer thought: Does the includion of this function for readability sake trump its redundency?
    for dates in datelist:
        Path.mkdir(Path(p) / dates)


def movethefiles(p, datelist):
    """
    Targets each file in the target path and moves it to its respective folder.
    """
    for dates in datelist:
        for pictures in datelist[dates]:
            os.rename(pictures, Path(p) / dates / pictures.name)
