#!/usr/bin/env python3

import ephem, random, math, io, os, sys, codecs
from datetime import datetime, timedelta
from math import sin, cos, asin, acos, degrees, radians

def gen_datetime(min_year=1900, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

def dd2dm(dd):
    add = abs(dd)
    d = int(add)
    m = 60 * (add - d)
    return "-" if dd < 0 else "", d,m


def format_degrees(dd):
    minus, d,m = dd2dm(dd)
    return minus + str(d) + "° " + "{:.1f}'".format(m).zfill(5)

def format_lat(dd):
    minus,d,m = dd2dm(dd)
    sign = "S " if minus == "-" else "N "
    return sign + "{:02d}° ".format(d) + "{:.1f}'".format(m).zfill(5)
		
def format_lon(dd):
    minus,d,m = dd2dm(dd)
    sign = "W " if minus == "-" else "E "
    return sign + "{:03d}° ".format(d) + "{:.1f}'".format(m).zfill(5)


# generate random position on earth
lat = random.randint(-75 * 1000, 75 * 1000) / 1000
lon = random.randint(-180 * 1000, 180 * 1000) / 1000

step1 = "Generating location ...\n" 

# setup observer
o = ephem.Observer()
o.lat = str(lat)
o.lon = str(lon)

# generate random date, make sure is is above horizon
step1 += "Generating date and time ..."
while True:
    y = datetime.now().year
    d = gen_datetime(y,y)
    o.date = d
    s = ephem.Sun(o)
    if s.alt > 0:
        break
    step1 += "."
step1 += "\n\n"

# prepare randomized assumed position
alat = lat + random.random() / 2 - 0.5
alon = lon + random.random() / 2 - 0.5

# STEP1: show GMT date, time, alt, assumed position
step1 += "UTC Date and time:   " + d.strftime("%Y-%m-%d %H:%M:%S") + "\n"

# add / substract limb
limb = random.randint(0,2)
Hs = s.alt
if limb == 0:
    Hs -= s.radius
    limb_str = "Lower"
if limb == 1:
    limb_str = "Center"
if limb == 2:
    Hs += s.radius
    limb_str = "Upper"

# add eye height
eh = random.randint(0,2)
if eh == 0:
    Hs += radians(2.5 / 60.0)
    eh_str = "2m"
if eh == 1:
    eh_str = "0m"
if eh == 2:
    Hs += radians(4.0 / 60.0)
    eh_str = "5m"

step1 += "Sextant Height (Hs): " + format_degrees(degrees(Hs)) + " Limb:" + limb_str + " Eye Height =" + eh_str + "\n"
step1 += "Assumed Latitude:    " + format_lat(alat) + "\n"
step1 += "Assumed Longitude:   " + format_lon(alon) + "\n"


# STEP2: show corrected alt, LHA, Dec
oo = o
oo.pressure = 0
so = ephem.Sun(oo)
step2 = "Observed Height (Ho):" + format_degrees(degrees(so.alt)) + "\n"

og = ephem.Observer()
og.date = d
GHA = og.sidereal_time() - s.g_ra
if GHA < 0: GHA += radians(360)

LHA = GHA + radians(alon)
if LHA > radians(360):
    LHA -= radians(360)
if LHA < 0:
    LHA += radians(360)

step2 += "GHA:                 " + format_degrees(degrees(GHA)) + "\n"
step2 += "LHA:                 " + format_degrees(degrees(LHA)) + "\n"
step2 += "Dec:                 " + format_lat(degrees(s.g_dec)) + "\n"

# STEP3: show Hc, Zn, position and assumed position

Hc = asin(sin(s.g_dec) * sin (radians(alat)) +
          cos(radians(alat)) * cos(s.g_dec) * cos(LHA))

Z = acos((sin(s.g_dec) - sin(radians(alat)) * sin(Hc)) /
           (cos(radians(alat)) * cos(Hc)))

if alat > 0:  # N lat
    if LHA > radians(180):
        Zn = Z
    else:
        Zn = radians(360) - Z
else:  # S lat
    if LHA > radians(180):
        Zn = radians(180) - Z
    else:
        Zn = radians(180) + Z 

step3 = "Hc:                  " +  format_degrees(degrees(Hc)) + "\n"
step3 += "Zn:                  " + format_degrees(degrees(Zn)) + "\n"


step3 += "Latitude:            " + format_lat(lat) + "\n"
step3 += "Longitude:           " + format_lon(lon) + "\n"

# OUTPUT

# set output to utf8
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print("Content-type: text/html")
print("Pragma: no-cache")
print("Cache-Control: no-cache")
print()
# read template
f = io.open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'cviceni.tpl'), encoding='utf-8')
templ = f.read()
f.close()

# output document
print(templ % {"step1": step1, "step2": step2, "step3": step3})
