from pathlib import Path
import datetime
import os


def whichfiles(p, filetype='image'):
    p = Path(whichdir(p))
    datelist = {}
    for files in p.iterdir():
        filedate = datetime.datetime.fromtimestamp(int(round(files.stat().st_mtime, -5)  )  )
        year, month, day = str(filedate.year), str(filedate.month), str(filedate.day)
        key = '-'.join([year, month, day])
        datelist.setdefault(key, []).append(files)
    return datelist


def whichdir(p, flag=0, filetype='image'):
    while True:
        if not Path.is_dir(Path(p)): p = input('Please input a valid path. Again, regular path types included (C:/ '
                                               '..., ~/ ..., ./ ..., ../ ...). Alternatively, to leave type "exit" ')
        if p == 'exit': exit()
        else: return p


def makethedirs(p, datelist):
    for dates in datelist:
        Path.mkdir(Path(p) / dates)


def movethefiles(p, datelist):
    for dates in datelist:
        for pictures in datelist[dates]:
            os.rename(pictures, Path(p) / dates / pictures.name)


p = input("Giz the path to the folder that requires sorting. Regular path types included (C:/ ..., ~/ ..., ./ ..., "
          "../ ...). ")
datelist = whichfiles(p)
makethedirs(p, datelist)
movethefiles(p, datelist)
