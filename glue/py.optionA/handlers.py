import pandas as pd
import numpy as np

from nptyping import NDArray, Datetime64  # type: ignore

# from dataenforce import Dataset
from typing import NewType, Dict, TypedDict, List, Iterable, Union
from numbers import Number

import os
import re
import numbers
import subprocess as sp
import tempfile as temp

from datetime import datetime
from functools import singledispatch
from io import StringIO
from math import cos
import urllib.request as urlreq


import logging

"""
Constants
"""

DEG2RAD = 3.14159 / 180
COLS = [
    "date",
    "GPST",
    "latitude",
    "longitude",
    "height",
    "Q",
    "ns",
    "sdn",
    "sde",
    "sdu",
    "sdne",
    "sdeu",
    "sdun",
    "age",
    "ratio",
]

"""
types
"""

GpstkDate = NewType("GpstkDate", str)
FilePath = NewType("FilePath", str)

bGpstkRinexSumary = NewType("bGpstkRinexSumary", bytes)
GpstkRinexSumary = NewType("GpstkRinexSumary", str)

RinexTimes = NewType("RinexTimes", Dict[str, Datetime64])
MarkerName = NewType("MarkerName", str)

"""
type validations
"""

"""
Loggers
"""

logDescargas = logging.getLogger("Descargas")
logGpstk = logging.getLogger("Gpstk")
logRtklib = logging.getLogger("Rtklib")

"""
---
"""


def totime(x: Iterable) -> Datetime64:
    return np.datetime64(datetime(*x))


# to_GPSTk_time :: np.datetime64 -> String
@singledispatch
def toGpstkTime(time: Datetime64) -> GpstkDate:
    datestring = "{},{},{},{},{},{}".format(*time.astype(datetime).timetuple())
    return GpstkDate(datestring)


@toGpstkTime.register(str)
def _(time: GpstkDate) -> GpstkDate:
    try:
        check = [int(i) for i in time.split(",")]
        # more checks
        return time
    except ValueError:
        raise ValueError("Bad gpstk time string")


def gpstkRinSum(path: FilePath, quiet: bool=False) -> bGpstkRinexSumary:
    if not quiet:
        logGpstk.info("Ejecutando RinSum para extraer información de {}".format(path))
    rinsumP = sp.run(["RinSum", path], capture_output=True)
    if rinsumP.stderr:
        logGpstk.warning(rinsumP.stderr.decode())
    if rinsumP.stdout:
        logGpstk.debug(rinsumP.stdout.decode())
    return bGpstkRinexSumary(rinsumP.stdout)


def gpstkSplitUntil(infile: FilePath, outfile: FilePath, time: Datetime64) -> bool:
    """
    Side-efects: Creation of output file at outfile
    """

    logGpstk.info("Ejecutando RinEdit: Cortando {} hasta {}".format(infile, time))

    rineditP = sp.run(
        ["RinEdit", "--IF", infile, "--OF", outfile, "--TE", toGpstkTime(time)],
        capture_output=True,
    )

    if rineditP.stderr:
        logGpstk.warning(rineditP.stderr.decode())
    if rineditP.stdout:
        logGpstk.debug(rineditP.stdout.decode())

    if isRinex(outfile):
        logGpstk.info("RinEdit: generado {}".format(outfile))
        return True
    else:
        raise ValueError("invalid output")


def gpstkSplitFrom(infile: FilePath, outfile: FilePath, time: Datetime64) -> bool:
    """
    Side-efects: Creation of output file at outfile
    """

    logGpstk.info("Ejecutando RinEdit: Cortando {} desde {}".format(infile, time))

    rineditP = sp.run(
        ["RinEdit", "--IF", infile, "--OF", outfile, "--TB", toGpstkTime(time)],
        capture_output=True,
    )

    if rineditP.stderr:
        logGpstk.warning(rineditP.stderr.decode())
    if rineditP.stdout:
        logGpstk.debug(rineditP.stdout.decode())

    if isRinex(outfile):
        logGpstk.info("RinEdit: generado {}".format(outfile))
        return True
    else:
        raise ValueError("invalid output")


# isRinex :: path -> Bool
def isRinex(path: FilePath) -> bool:
    logGpstk.info("Usando RinSum para chequear la validez de {}".format(path))
    if gpstkRinSum(path,quiet=True).find(b"This header is VALID") == -1:
        return False
    else:
        return True


# parse_times :: RinSum output -> [time,time,time]
@singledispatch
def parse_times(rxSum: List[str]) -> RinexTimes:
    ini_time: Datetime64 = None
    end_time: Datetime64 = None

    for i in rxSum:
        if m := re.match(
            r".*first\s+epoch:\s+(\d+).(\d+).(\d+).*?(\d+).(\d+).(\d+).*?=.*?(\d+)\s+(\d+)\s+([\d\.]+)",
            i,
        ):
            ini_time = totime((int(i) for i in m.groups()[:6]))
        if m := re.match(
            r".*last\s+epoch:\s+(\d+).(\d+).(\d+).*?(\d+).(\d+).(\d+).*?=.*?(\d+)\s+(\d+)\s+([\d\.]+)",
            i,
        ):
            end_time = totime((int(i) for i in m.groups()[:6]))

    try:
        medio_st = ini_time + (end_time - ini_time) / 2
    except TypeError:
        raise ValueError("Summary doesn't have proper start and end times")

    return RinexTimes({"start": ini_time, "mid": medio_st, "end": end_time})


@parse_times.register(bytes)  # type: ignore[no-redef]
def _(bytesRxSum: bGpstkRinexSumary) -> RinexTimes:
    return parse_times(bytesRxSum.decode())


@parse_times.register(str)  # type: ignore[no-redef]
def _(stringRxSum: GpstkRinexSumary) -> RinexTimes:
    return parse_times(stringRxSum.splitlines())

@singledispatch
def parse_marker(bytesRxSum: bGpstkRinexSumary) -> MarkerName:
    token = b'Marker name: '
    start = bytesRxSum.index(token) + len(token)
    end = start + 4
    name = MarkerName( bytesRxSum[start:end].decode() )

    return name

@parse_marker.register(str)  # type: ignore[no-redef]
def _(stringRxSum: GpstkRinexSumary) -> MarkerName:
    token = 'Marker name: '
    start = stringRxSum.index(token) + len(token)
    end = start + 4
    name = MarkerName( stringRxSum[start:end] )

    return name

def gpstkPRSolveGC1(obs: FilePath, nav: FilePath, outfile: FilePath) -> bool:

    logGpstk.info(
        "Ejecutando PRSolve: calculando solución L1 autonoma de {}".format(obs)
    )

    prsolve = sp.run(
        ["PRSolve", "--obs", obs, "--nav", nav, "--sol", "GPS:1:C", "--log", outfile],
        capture_output=True,
    )

    if prsolve.stderr:
        logGpstk.warning(prsolve.stderr.decode())
    if prsolve.stdout:
        logGpstk.debug(prsolve.stdout.decode())

    # TODO: check valid solution
    return True


@singledispatch
def timeconvertFrom(
    data: List[Number], fmt: str = None, customFormat: str = None
) -> Datetime64:

    # convert numbers to strings for commandline parsing
    strdata = [str(i) for i in data]

    if not fmt is None:
        tout = sp.check_output(
            [
                "timeconvert",
                "--{}".format(fmt),
                " ".join(strdata),
                "-F",
                "%Y %m %d %H %M %S",
            ]
        )
    elif not customFormat is None:
        raise TypeError("when using customFormat data must be string")
    else:
        raise ValueError("must provide format")

    return totime([int(i) for i in tout.split()])


@timeconvertFrom.register(str)  # type: ignore[no-redef]
def _(data: str, fmt: str = None, customFormat: str = None) -> Datetime64:

    if not fmt is None:
        tout = sp.check_output(
            ["timeconvert", "--{}".format(fmt), data, "-F", "%Y %m %d %H %M %S"]
        )
    elif not customFormat is None:
        tout = sp.check_output(
            [
                "timeconvert",
                "--input-format",
                customFormat,
                "--input-time",
                data,
                "-F",
                "%Y %m %d %H %M %S",
            ]
        )
    else:
        raise ValueError("must provide format")

    return totime([int(i) for i in tout.split()])


def timeconvertTo(data: Datetime64, fmt: str) -> List[str]:
    date = np.datetime64(data, "s")
    tout = sp.check_output(
        [
            "timeconvert",
            "--input-format",
            "%Y-%m-%dT%H:%M:%S",
            "--input-time",
            str(data),
            "-F",
            fmt,
        ]
    )
    return tout.decode().split()


def gpstkPRSol_ParseDOP(solfile: FilePath) -> pd.Series:

    logGpstk.info("Cargando Pdop: desde la solucion autonoma de {}".format(solfile))

    filtered = sp.check_output(["grep", "RPF GPS:1:C RMS", solfile])

    fstlineend = filtered.index(b"\n")
    fstline = filtered[:fstlineend].split()
    week = int(fstline[3])
    sow = float(fstline[4])

    initime = timeconvertFrom([week, sow], fmt="ws")

    PDOP = pd.read_fwf(StringIO(filtered.decode()), header=None).set_index(4).loc[:, 8]

    PDOP.index = initime + (PDOP.index - PDOP.index[0]) * np.timedelta64(1, "s")

    return PDOP


def gpskRinEditPdopFilter(
    file: FilePath,
    pdop: pd.Series = None,
    outfile: FilePath = None,
    max_pdop: float = 2.5,
    nav: FilePath = None,
) -> FilePath:

    if pdop is None:
        with temp.TemporaryDirectory() as tmpdir:

            if nav is None:
                nav = getBrdcNav(file)[0]
            nav = FilePath(nav)

            solfile = os.path.join(tmpdir, "solution.sol")
            solfile = FilePath(solfile)

            gpstkPRSolveGC1(file, nav, solfile)

            pdop = gpstkPRSol_ParseDOP(solfile)

    mask: NDArray[bool] = pdop.values > max_pdop

    malos = pdop[mask].index

    starts = malos[1:][((malos[1:] - malos[:-1]) / np.timedelta64(1, "s")).values > 1]
    starts = pd.Index(np.concatenate([malos[:1], starts]))
    stops = malos[:-1][((malos[1:] - malos[:-1]) / np.timedelta64(1, "s")).values > 1]
    stops = pd.Index(np.concatenate([stops, malos[-1:]]))

    breaks = []
    for b, e in zip(starts, stops):
        b = np.datetime64(b)
        e = np.datetime64(e)
        if e == b:
            breaks.append("--DA {}".format(toGpstkTime(b)))
        else:
            breaks.append(
                "--DA+ {} --DA- {}".format(
                    toGpstkTime(b), toGpstkTime(e + np.timedelta64(1, "s"))
                )
            )

    # basedir = os.path.join(os.path.dirname(self.path),'pdop-cleaned')
    #!mkdir -p {basedir}

    outfile = checkPath(outfile, 1)

    logGpstk.info(
        "Filtrando {}: eliminando epocas con pdop > {}".format(file, max_pdop)
    )

    rineditP = sp.run(
        ["RinEdit", "--IF", file, "--OF", outfile, *" ".join(breaks).split()],
        capture_output=True,
    )

    if rineditP.stderr:
        logGpstk.warning(rineditP.stderr.decode())
    if rineditP.stdout:
        logGpstk.debug(rineditP.stdout.decode())

    if isRinex(outfile):
        return outfile
    else:
        raise ValueError("inalid output")


@singledispatch
def checkPath(path: FilePath, depth: int) -> FilePath:
    if depth < 0:
        raise ValueError("Too Deep")

    dirpath = os.path.dirname(path)

    if os.path.isdir(dirpath):
        return path
    else:
        return checkPath([path, dirpath], depth - 1)


@checkPath.register(list)  # type: ignore[no-redef]
def _(path: List[FilePath], depth: int) -> FilePath:
    if depth < 0:
        raise ValueError("Too Deep")

    if len(path) == 1:
        return checkPath(path[0], depth=depth)

    dirpath = os.path.dirname(path[-1])

    if os.path.isdir(dirpath):
        os.mkdir(path[-1], mode=0o755)
        return checkPath(path[:-1], depth=depth)
    else:
        return checkPath([*path, dirpath], depth=depth - 1)


def rtklibDifSol(
    punto: FilePath,
    base: FilePath,
    conf: FilePath,
    output: FilePath,
    extra_args: List[str] = [],
    nav: Union[FilePath, List[FilePath]] = None,
    eph: Union[FilePath, List[FilePath]] = None,
) -> int:

    if isinstance(nav, str):
        nav = [nav]
    if nav is None:
        nav = getBrdcNav(punto)
    if isinstance(eph, str):
        eph = [eph]
    if eph is None:
        eph = []

    logRtklib.info("Resolviendo vector con RTKLIB: ")
    logRtklib.info("Archivo Base: {}".format(base))
    logRtklib.info("Archivo Rotador: {}".format(punto))
    logRtklib.info("Archivo de Configuración: {}".format(conf))

    rtkproc = sp.run(
        ["rnx2rtkp", *extra_args, "-k", conf, punto, base, *nav, *eph, "-o", output],
        capture_output=True,
    )

    if rtkproc.stderr:
        logRtklib.warning(rtkproc.stderr.decode())
    if rtkproc.stdout:
        logRtklib.debug(rtkproc.stdout.decode())
    # run checks
    return rtkproc.returncode


@singledispatch
def getBrdcNav(file: FilePath, times: Dict[str, Datetime64] = None) -> List[FilePath]:

    logDescargas.info("Buscando archivo de navegación para {}".format(file))

    if times is None:
        times = parse_times(gpstkRinSum(file,quiet=True))

    ini_y, ini_doy = timeconvertTo(times["start"], "%Y %j")
    end_y, end_doy = timeconvertTo(times["end"], "%Y %j")

    url = "ftp://igs.ensg.ign.fr/pub/igs/data/{}/{:03d}/brdc{:03d}0.{}n.Z".format(
        ini_y, int(ini_doy), int(ini_doy), ini_y[2:]
    )

    logDescargas.info("Descargando {}".format(url))

    weburl = urlreq.urlopen(url)
    data = weburl.read()
    dest_path = file[:-1] + "n"

    files = []
    with open(dest_path, "bw") as f:
        sp.run("gunzip", input=data, stdout=f)
    files.append(FilePath(dest_path))

    if ini_doy != end_doy:
        url = "ftp://igs.ensg.ign.fr/pub/igs/data/{}/{:03d}/brdc{:03d}0.{}n.Z".format(
            end_y, int(end_doy), int(end_doy), end_y[2:]
        )
        logDescargas.info("Descargando {}".format(url))

        weburl = urlreq.urlopen(url)
        data = weburl.read()
        dest_path = file[:-4] + "+." + end_y[2:] + "n"

        with open(dest_path, "bw") as f:
            sp.run("gunzip", input=data, stdout=f)
        files.append(FilePath(dest_path))

    return files


class DataFile(object):
    def __init__(self, file):
        self.path = file
        self.p1path = None
        self.p2path = None
        self._sumary = gpstkRinSum(self.path)
        self.times = parse_times(self._sumary)
        self.sess = {}
        self.sessData = {}

    def mid_split(self, folder):
        file = os.path.basename(self.path)
        self.p1path = os.path.join(folder, file.replace("0.", "1."))
        self.p2path = os.path.join(folder, file.replace("0.", "2."))
        # m = toGpstkTime(self.times['mid'])

        gpstkSplitUntil(self.path, self.p1path, self.times["mid"])
        gpstkSplitFrom(self.path, self.p2path, self.times["mid"])

    def _compute_pdop(self, nav=None, part=0):

        path = {0: self.path, 1: self.p1path, 2: self.p2path}.get(part, None)

        if path is None:
            raise ValueError("Attemp to read an uninitialized part")

        with temp.TemporaryDirectory() as tmpdir:

            basepath = ".".join(path.split(".")[:-1])
            basepath = os.path.join(tmpdir, os.path.basename(basepath))

            if nav is None:
                nav = path[:-1] + "n"

            gpstkPRSolveGC1(path, nav, "{}.sol".format(basepath))

            pdop: pd.Series = gpstkPRSol_ParseDOP("{}.sol".format(basepath))

        return pdop

    def store_pdops(self, nav=None):
        self.pdop = self._compute_pdop(nav=nav, part=0)
        try:
            self.p1pdop = self._compute_pdop(nav=nav, part=1)
            self.p2pdop = self._compute_pdop(nav=nav, part=2)
        except ValueError as e:
            # print("WARNING:{}".format(e))
            pass

        return True

    def _pdop_filter(self, max_pdop=2.5):

        outdir = os.path.dirname(self.path)
        outfile = "filt_{}".format(os.path.basename(self.path))

        outpath = os.path.join(outdir, outfile)

        gpskRinEditPdopFilter(self.path, pdop=self.pdop, outfile=outpath, max_pdop=2.5)

        return DataFile(outpath)

    def process(self, base, conf, sp3=[], nav=None, session=None, folder=None):
        if session == None:
            for i in range(3):
                self.process(base, conf, session=i, sp3=sp3, nav=nav, folder=folder)
            return True

        path = {0: self.path, 1: self.p1path, 2: self.p2path}.get(session, None)

        if path is None:
            raise ValueError("Attemp to read an uninitialized part")

        basepath = ".".join(path.split(".")[:-1])

        if nav is None:
            nav = path[:-1] + "n"

        if folder == None:
            folder = os.path.join(os.path.dirname(self.path), "sesiones")

        punto = path
        base = base.path
        eph = ["{}".format(i) for i in set(sp3)]
        sessname = "{}-{}-{}".format(
            os.path.basename(base)[:4], os.path.basename(path)[:4], session
        )
        output = os.path.join(folder, sessname)

        # Create directory if needed
        output = checkPath(output, depth=1)

        fwsess = rtklibDifSol(
            punto,
            base,
            conf,
            "{}-fw.txt".format(output),
            extra_args=[],
            nav=[nav],
            eph=eph,
        )

        if not fwsess == 0:
            raise ValueError("rtklib returned not 0 error code")

        self.sess["{}-fw".format(session)] = "{}-fw.txt".format(output)

        #!echo rnx2rtkp -k {conf} {punto} {base} {nav} {eph} -o {output}-fw.txt
        #!rnx2rtkp -k {conf} {punto} {base} {nav} {eph} -o {output}-fw.txt

        bwsess = rtklibDifSol(
            punto,
            base,
            conf,
            "{}-bw.txt".format(output),
            extra_args=["-b"],
            nav=[nav],
            eph=eph,
        )

        if not bwsess == 0:
            raise ValueError("rtklib returned not 0 error code")

        self.sess["{}-bw".format(session)] = "{}-bw.txt".format(output)

        #!echo rnx2rtkp -b -k {conf} {punto} {base} {nav} {eph} -o {output}-bw.txt
        #!rnx2rtkp -b -k {conf} {punto} {base} {nav} {eph} -o {output}-bw.txt

        return True

    def reloadProcesed(self):
        for k, v in self.sess.items():
            sess = pd.read_fwf(v, comment="%", names=COLS, index=None)
            sess = sess.set_index(
                (sess.date + "T" + sess.GPST).map(
                    lambda x: np.datetime64(x.replace("/", "-"))
                )
            )
            self.sessData[k] = sess

        return True


@getBrdcNav.register(DataFile)  # type: ignore[no-redef]
def _(file: DataFile, times: Dict[str, Datetime64] = None) -> List[FilePath]:
    return getBrdcNav(file.path, file.times)
