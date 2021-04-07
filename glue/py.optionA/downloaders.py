from .handlers import FilePath, DataFile, timeconvertTo, checkPath

from typing import List

import urllib.request as urlreq
import os
import subprocess


def saveSp3(w: str, d: str, folder: FilePath = FilePath(".")) -> FilePath:
    url = "ftp://gssc.esa.int/gnss/products/{}/igs{}.sp3.Z".format(w, d)
    weburl = urlreq.urlopen(url)
    data = weburl.read()
    dest_path = os.path.join(folder, "igs{}.sp3".format(d))
    dest_path = checkPath(FilePath(dest_path), depth=1)
    with open(dest_path, "bw") as f:
        subprocess.run("gunzip", input=data, stdout=f)
    return FilePath(dest_path)


def getPreciseEphs(file: DataFile, folder: FilePath = FilePath(".")) -> List[FilePath]:

    wdTime = timeconvertTo(file.times["start"], "%F %w")

    iniw, inid = [int(i) for i in wdTime]

    sp3files = []

    w = "{}".format(iniw)
    d = "{}{}".format(iniw, inid)
    sp3files.append(saveSp3(w, d, folder))

    if inid == 0:
        w = "{}".format(iniw - 1)
        d = "{}{}".format(iniw - 1, 6)
        sp3files.append(saveSp3(w, d, folder))
        w = "{}".format(iniw)
        d = "{}{}".format(iniw, 1)
        sp3files.append(saveSp3(w, d, folder))
    elif inid == 6:
        w = "{}".format(iniw)
        d = "{}{}".format(iniw, 5)
        sp3files.append(saveSp3(w, d, folder))
        w = "{}".format(iniw)
        d = "{}{}".format(iniw + 1, 0)
        sp3files.append(saveSp3(w, d, folder))
    else:
        w = "{}".format(iniw)
        d = "{}{}".format(iniw, inid + 1)
        sp3files.append(saveSp3(w, d, folder))
        w = "{}".format(iniw)
        d = "{}{}".format(iniw, inid - 1)
        sp3files.append(saveSp3(w, d, folder))

    return sp3files
