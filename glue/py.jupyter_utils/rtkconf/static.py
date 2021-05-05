# rtkpost options (2010/08/07 09:24:29, v.2.4.0)
from ipywidgets import Dropdown as __Dropdown, SelectMultiple as __SelectMultiple

pos1_posmode = __Dropdown(
    value="3:static",
    options=[
        "0:single",
        "1:dgps",
        "2:kinematic",
        "3:static",
        "4:movingbase",
        "5:fixed",
        "6:ppp-kine",
        "7:ppp-static",
        "8:ppp-fixed",
    ],
    description="pos1-posmode",
)
pos1_frequency = __Dropdown(
    value="1:l1",
    options=["1:l1", "2:l1+l2", "3:l1+l2+l5", "4:l1+l2+l5+l6", "5:l1+l2+l5+l6+l7"],
    description="pos1-frequency",
)
pos1_soltype = __Dropdown(
    value="2:combined",
    options=["0:forward", "1:backward", "2:combined"],
    description="pos1-soltype",
)
pos1_elmask = 10  # (deg)
pos1_snrmask = 0  # (dBHz)
pos1_dynamics = __Dropdown(
    value="1:on", options=["0:off", "1:on"], description="pos1-dynamics"
)
pos1_tidecorr = __Dropdown(
    value="1:on", options=["0:off", "1:on"], description="pos1-tidecorr"
)
pos1_ionoopt = __Dropdown(
    value="0:off",
    options=[
        "0:off",
        "1:brdc",
        "2:sbas",
        "3:dual-freq",
        "4:est-stec",
        "5:ionex-tec",
        "6:qzs-brdc",
        "7:qzs-lex",
        "8:vtec_sf",
        "9:vtec_ef",
        "10:gtec",
    ],
    description="pos1-ionoopt",
)
pos1_tropopt = __Dropdown(
    value="1:saas",
    options=["0:off", "1:saas", "2:sbas", "3:est-ztd", "4:est-ztdgrad"],
    description="pos1-tropopt",
)
pos1_sateph = __Dropdown(
    value="0:brdc",
    options=["0:brdc", "1:precise", "2:brdc+sbas", "3:brdc+ssrapc", "4:brdc+ssrcom"],
    description="pos1-sateph",
)
pos1_exclsats = ""  # (prn ...)
pos1_navsys = __Dropdown(
    value="1:gps",
    options=[
        "1:gps",
        "2:sbas",
        "3:gps+sbas",
        "4:glo",
        "5:gps+glo",
        "6:sbas+glo",
        "7:gps+sbas+glo",
        "8:gal",
        "9:gps+gal",
        "10:sbas+gal",
        "11:gps+sbas+gal",
        "12:glo+gal",
        "13:gps+glo+gal",
        "14:sbas+glo+gal",
        "15:gps+sbas+glo+gal",
        "16:qzs",
        "17:gps+qzs",
        "18:sbas+qzs",
        "19:gps+sbas+qzs",
        "20:glo+qzs",
        "21:gps+glo+qzs",
        "22:sbas+glo+qzs",
        "23:gps+sbas+glo+qzs",
        "24:gal+qzs",
        "25:gps+gal+qzs",
        "26:sbas+gal+qzs",
        "27:gps+sbas+gal+qzs",
        "28:glo+gal+qzs",
        "29:gps+glo+gal+qzs",
        "30:sbas+glo+gal+qzs",
        "31:gps+sbas+glo+gal+qzs",
        "32:comp",
    ],
    description="pos1-navsys",
)
pos2_armode = __Dropdown(
    value="3:fix-and-hold",
    options=["0:off", "1:continous", "2:instantaneous", "3:fix-and-hold"],
    description="pos2-armode",
)
pos2_gloarmode = __Dropdown(
    value="1:on", options=["0:off", "1:on", "2:autocal"], description="pos2-gloarmode"
)
pos2_arthres = 5
pos2_arlockcnt = 10
pos2_arelmask = 20  # (deg)
pos2_aroutcnt = 1
pos2_arminfix = 30
pos2_elmaskhold = 15
pos2_slipthres = 0.05  # (m)
pos2_maxage = 30  # (s)
pos2_rejionno = 30  # (m)
pos2_niter = 5
pos2_baselen = 0  # (m)
pos2_basesig = 0  # (m)
out_solformat = __Dropdown(
    value="0:llh",
    options=["0:llh", "1:xyz", "2:enu", "3:nmea"],
    description="out-solformat",
)
out_outhead = __Dropdown(
    value="1:on", options=["0:off", "1:on"], description="out-outhead"
)
out_outopt = __Dropdown(
    value="1:on", options=["0:off", "1:on"], description="out-outopt"
)
out_timesys = __Dropdown(
    value="0:gpst", options=["0:gpst", "1:utc", "2:jst"], description="out-timesys"
)
out_timeform = __Dropdown(
    value="1:hms", options=["0:tow", "1:hms"], description="out-timeform"
)
out_timendec = 3
out_degform = __Dropdown(
    value="0:deg", options=["0:deg", "1:dms"], description="out-degform"
)
out_fieldsep = ""
out_height = __Dropdown(
    value="0:ellipsoidal",
    options=["0:ellipsoidal", "1:geodetic"],
    description="out-height",
)
out_geoid = __Dropdown(
    value="0:internal",
    options=["0:internal", "1:egm96", "2:egm08_2.5", "3:egm08_1", "4:gsi2000"],
    description="out-geoid",
)
# out_solstatic      =all        # (0:all,1:single)
out_solstatic = __Dropdown(
    value="0:all", options=["0:all", "1:single"], description="out-solstatic"
)
out_nmeaintv1 = 0  # (s)
out_nmeaintv2 = 0  # (s)
out_outstat = __Dropdown(
    value="2:residual",
    options=["0:off", "1:state", "2:residual"],
    description="out-outstat",
)
stats_errratio = 100
stats_errphase = 0.003  # (m)
stats_errphaseel = 0.003  # (m)
stats_errphasebl = 0  # (m/10km)
stats_errdoppler = 10  # (Hz)
stats_stdbias = 30  # (m)
stats_stdiono = 0.03  # (m)
stats_stdtrop = 0.3  # (m)
stats_prnaccelh = 0.1  # (m/s^2)
stats_prnaccelv = 0.01  # (m/s^2)
stats_prnbias = 0.0001  # (m)
stats_prniono = 0.001  # (m)
stats_prntrop = 0.0001  # (m)
stats_clkstab = 5e-12  # (s/s)
ant1_postype = __Dropdown(
    value="2:single",
    options=["0:llh", "1:xyz", "2:single", "3:posfile", "4:rinexhead", "5:rtcm"],
    description="ant1-postype",
)
ant1_pos1 = 0.  # (deg|m)
ant1_pos2 = 0.  # (deg|m)
ant1_pos3 = 0.  # (m|m)
ant1_anttype = "*"
ant1_antdele = 0.  # (m)
ant1_antdeln = 0.  # (m)
ant1_antdelu = 0.  # (m)
ant2_postype = __Dropdown(
    value="3:posfile",
    options=["0:llh", "1:xyz", "2:single", "3:posfile", "4:rinexhead", "5:rtcm"],
    description="ant2-postype",
)
ant2_pos1 = 0.  # (deg|m)
ant2_pos2 = 0.  # (deg|m)
ant2_pos3 = 0.  # (m|m)
ant2_anttype = "*"
ant2_antdele = 0.  # (m)
ant2_antdeln = 0.  # (m)
ant2_antdelu = 0.  # (m)
misc_timeinterp = __Dropdown(
    value="1:on", options=["0:off", "1:on"], description="misc-timeinterp"
)
misc_sbasatsel = 0  # (0:all)
file_satantfile = "/data/igs05.atx"
file_rcvantfile = "/data/igs05.atx"
file_staposfile = "/data/ramsac.pos"
file_geoidfile = ""
file_dcbfile = "/data/P1C1_ALL.DCB"
file_tempdir = ""
file_geexefile = ""
file_solstatfile = ""
file_tracefile = ""
