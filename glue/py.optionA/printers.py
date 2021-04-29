import pandas as pd
import matplotlib.pyplot as plt  # type: ignore

# from dataenforce import Dataset

from math import cos
from itertools import cycle
from .handlers import DataFile

"""
Constants
"""

DEG2RAD = 3.14159 / 180


def plot_latitude(sess, ax=None, filtro=lambda x: x.iloc[len(x) // 2 :], **kwargs):
    if ax is None:
        fig, ax = plt.subplots()
    filtro(sess.latitude * DEG2RAD * 6.4e6).plot(ax=ax, **kwargs)
    return ax


def plot_longitude(sess, ax=None, filtro=lambda x: x.iloc[len(x) // 2 :], **kwargs):
    reflat = sess.latitude.median()
    cosreflat = cos(reflat * DEG2RAD)

    if ax is None:
        fig, ax = plt.subplots()

    filtro(sess.longitude * DEG2RAD * cosreflat * 6.4e6).plot(ax=ax, **kwargs)
    return ax


def plot_height(sess, ax=None, filtro=lambda x: x.iloc[len(x) // 2 :], **kwargs):

    if ax is None:
        fig, ax = plt.subplots()

    filtro(sess.height).plot(ax=ax, **kwargs)
    return ax


def plot_track(sess, ax=None, filtro=lambda x: x.iloc[len(x) // 2 :], **kwargs):
    reflat = sess.latitude.median()
    cosreflat = cos(reflat * DEG2RAD)

    if ax is None:
        fig, ax = plt.subplots()

    ax.plot(
        filtro(sess).longitude * DEG2RAD * cosreflat * 6.4e6,
        filtro(sess).latitude * DEG2RAD * 6.4e6,
        **kwargs,
    )

    ax.set_aspect("equal")
    return ax


def plot_last(sess, ax=None, filtro=lambda x: x.iloc[len(x) // 2 :], **kwargs):
    reflat = sess.latitude.median()
    cosreflat = cos(reflat * DEG2RAD)

    if ax is None:
        fig, ax = plt.subplots()

    ax.plot(
        sess.longitude[-1] * DEG2RAD * cosreflat * 6.4e6,
        sess.latitude[-1] * DEG2RAD * 6.4e6,
        **kwargs,
    )

    ax.set_aspect("equal")
    return ax


def plot_tracks(sessions, filtro=lambda x: x.iloc[len(x) // 2 :]):
    fig, ax = plt.subplots()
    for sess, mk1, mk2 in zip(sessions, cycle(["x", ".", "^"]), cycle([">", "o", "^"])):
        plot_track(sess, ax=ax, filtro=filtro, marker=mk1, alpha=0.05)
        plot_last(sess, ax=ax, marker=mk2, markersize=15)

    plt.show()

def GEOBA_final_pos(data: DataFile) -> pd.DataFrame:

    posiciones = []
    for run in range(3):
        posFw = data.sessData['{}-fw'.format(run)]
        posFw = {'latitud':posFw.latitude[-1],
                 'longitud':posFw.longitude[-1],
                 'altura':posFw.height[-1]
                }
        posBw = data.sessData['{}-bw'.format(run)]
        posBw = {'latitud':posBw.latitude[-1],
                 'longitud':posBw.longitude[-1],
                 'altura':posBw.height[-1]
                }

        posiciones.append({k:(posFw[k]+posBw[k])/2 for k in posFw.keys()})

    sesiones = ["{longitud} {latitud} {altura}".format(**d) for d in posiciones]

    sesiones_string = '\n'.join(['',*sesiones,'EOF',''])

    #TODO: Select projection
    proyeccion = "+proj=tmerc +ellps=GRS80 +lat_0=-90 +lon_0=-60 +x_0=5500000 +no_defs"

    projout = pd.DataFrame(\
                  np.array([i.split() for i in\
                            sp.check_output(['proj','-f','%.3f',*proyeccion.split()],
                                            input='\n'.join(sesiones).encode()
                                           ).splitlines()\
                           ]).astype(float),
                           index=['Sesion Completa','Sesion 1','Sesion 2'],
                           columns=['Este','Norte','Altura']
                          )

    return projout

