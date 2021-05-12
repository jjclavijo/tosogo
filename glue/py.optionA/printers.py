import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns

# from dataenforce import Dataset

from math import cos,floor
from itertools import cycle
from .handlers import DataFile

from typing import Tuple,Optional
from numbers import Number

import subprocess as sp

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

    filtro(sess).height.plot(ax=ax, **kwargs)
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
        filtro(sess).longitude[-1] * DEG2RAD * cosreflat * 6.4e6,
        filtro(sess).latitude[-1] * DEG2RAD * 6.4e6,
        **kwargs,
    )

    ax.set_aspect("equal")
    return ax

def plot_median(sess, ax=None, filtro=lambda x: x.iloc[len(x) // 2 :], **kwargs):
    reflat = sess.latitude.median()
    cosreflat = cos(reflat * DEG2RAD)

    if ax is None:
        fig, ax = plt.subplots()

    ax.plot(
        filtro(sess).longitude.median() * DEG2RAD * cosreflat * 6.4e6,
        filtro(sess).latitude.median() * DEG2RAD * 6.4e6,
        **kwargs,
    )

    ax.set_aspect("equal")
    return ax


def plot_tracks(sessions, ax=None, filtro=lambda x: x.iloc[len(x) // 2 :]):
    if ax is None:
        fig, ax = plt.subplots()

    for sess, mk1, mk2 in zip(sessions, cycle(["x", ".", "^"]), cycle([">", "o", "^"])):
        plot_track(sess, ax=ax, filtro=filtro, marker=mk1, alpha=0.05)
        plot_last(sess, ax=ax, filtro=filtro, marker=mk2, markersize=15)

    return ax #plt.show()

def deg2dms(deg:Number) -> Tuple[int,int,float]:
    d: int
    m: int
    s: float

    side: int = -1 if deg < 0 else 1
    deg = abs(deg)
    d = floor(deg)
    _m = deg - d
    _m *= 60
    m = floor(_m)
    _s = _m - m
    _s *= 60
    s = _s

    return d*side, m, s

def GEOBA_final_pos(data: DataFile, proj: Optional[str]='GEOBA',filtro= lambda x: x) -> pd.DataFrame:

    posiciones = []
    for run in range(3):
        posFw = data.sessData['{}-fw'.format(run)]

        posFw = filtro(posFw)

        posFw = {'latitud':posFw.latitude.values,
                 'longitud':posFw.longitude.values,
                 'altura':posFw.height.values
                }

        posBw = data.sessData['{}-bw'.format(run)]
        posBw = filtro(posBw)

        posBw = {'latitud':posBw.latitude.values,
                 'longitud':posBw.longitude.values,
                 'altura':posBw.height.values
                }

        posiciones.append({k:np.median(np.concatenate([posFw[k],posFw[k]])) for k in posFw.keys()})


    if proj is None:
        out = pd.DataFrame(posiciones,
                index=['Sesion Completa','Sesion 1','Sesion 2'])

    elif proj is 'geograficas':

        out = pd.DataFrame(posiciones,
                index=['Sesion Completa','Sesion 1','Sesion 2'])

        out.loc[:,['latitud','longitud']] = out.loc[:,['latitud','longitud']]\
                                               .applymap(lambda x:
                                                       '{}°{}\'{:.5f}\"'\
                                                       .format(*deg2dms(x)))

    else:
        sesiones = ["{longitud} {latitud} {altura}".format(**d) for d in posiciones]
        sesiones_string = '\n'.join(['',*sesiones,'EOF',''])

        if proj == 'GEOBA':
            #TODO: Select projection
            proyeccion = "+proj=tmerc +ellps=GRS80 +lat_0=-90 +lon_0=-60 +x_0=5500000 +no_defs"
        else:
            proyeccion = proj

        #TODO: Check projections
        out = pd.DataFrame(\
                  np.array([i.split() for i in\
                            sp.check_output(['proj','-f','%.3f',*proyeccion.split()],
                                            input='\n'.join(sesiones).encode()
                                           ).splitlines()\
                           ]).astype(float),
                           index=['Sesion Completa','Sesion 1','Sesion 2'],
                           columns=['Este','Norte','Altura']
                          )

    return out


def filtroQ(x):
    mask = x.Q == 1
    return x.loc[mask.values]

def filtroGauss(x):

    df = x.copy()

    #df.longitude *= 6400000  * DEG2RAD * np.cos(df.iloc[0].latitude * DEG2RAD )
    #df.latitude *= 6400000 * DEG2RAD

    mask = (( df.latitude < (-df.latitude.std()*3+df.latitude.median()) )    |\
            ( df.latitude > (df.latitude.std()*3+df.latitude.median()) )     |\
            ( df.longitude < (-df.longitude.std()*3+df.longitude.median()) ) |\
            ( df.longitude > (df.longitude.std()*3+df.longitude.median()) )  |\
            ( df.height < (-df.height.std()*3+df.height.median()) )          |\
            ( df.height > (df.height.std()*3+df.height.median()) )            \
            )

    #mask.sum()
    #logger.log(f'filtering {mask.sum()} epochs')
    df = df[~mask]
    return df

def plotSessionGraphs(data,filtro=lambda x: x): #sessdata -> None

    def f(k,x):
        df = filtro(x)
        df.loc[:,'sesn'] = k
        return df

    df = pd.concat(map(lambda x:f(*x), data.items()))

    reflat = df.latitude.median()

    df.longitude *= 6400000  * DEG2RAD * np.cos(reflat * DEG2RAD )
    df.latitude *= 6400000 * DEG2RAD

    df.loc[:,'sesion'] = df.loc[:,'sesn'].apply(lambda x: x.split('-')[0])
    df.loc[:,'corrida'] = df.loc[:,'sesn'].apply(lambda x: x.split('-')[1])

    normlat = np.median(df.loc[df.sesion == '0','latitude'].values)
    normlon = np.median(df.loc[df.sesion == '0','longitude'].values)

    df.latitude -= normlat
    df.longitude -= normlon

    ax = sns.kdeplot(data=df,x='latitude',y='longitude',hue='sesion',
                     gridsize=60,bw_adjust=4,palette='tab10', levels=[0.33])

    ax = sns.kdeplot(data=df,x='latitude',y='longitude',hue='sesion',
                     gridsize=60,bw_adjust=4,palette='tab10',
                     ax=ax, levels=[0.05],linestyles='dashed')

    ax.set_aspect('equal')

    handles = ax.get_children()[:6]
    labels = ['2σ: Completo','2σ:Sesion 1','2σ: Sesion 2',
              '95%: Completo','95%:Sesion 1','95%: Sesion 2']

    ax.legend(handles=handles,labels=labels,ncol=3,loc=3)

    plt.show()

    ax = sns.violinplot(data=df, y='height',x='sesion',hue='corrida'
                        ,palette='tab10', split=True, scale='area'
                        , common_norm=False, common_grid=True
                    )

    ax.legend(loc=4)

    plt.show()
