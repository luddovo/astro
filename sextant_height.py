#!/usr/bin/env python3

import sys, codecs, io, os, urllib.parse, ephem, datetime, math

# READ QUERY PARAMETERS

qs = os.environ.get("QUERY_STRING", "")

form_fields = urllib.parse.parse_qs(qs, True)

# SET UP FORM FIELDS (DEFAULTS OR FROM QS)

field_lat = form_fields['lat'][0] if "lat" in form_fields else ''
field_lon = form_fields['lon'][0] if "lon" in form_fields else ''
field_date = form_fields['date'][0] if "date" in form_fields else ''
field_time = form_fields['time'][0] if "time" in form_fields else ''
field_limb = form_fields['limb'][0] if "limb" in form_fields else ''
field_eye_height = form_fields['eye_height'][0] if "eye_height" in form_fields else ''
field_fetch = form_fields['fetch'][0] if "fetch" in form_fields else ''

hs = ''

if "submit" in form_fields:
    # process

    # setup observer
    o = ephem.Observer()
    o.lat = str(field_lat)
    o.lon = str(field_lon)
    
    dt = field_date + 'T' + field_time + "Z"
    o.date = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
    s = ephem.Sun(o)
    
    #limb
    hs = s.alt
    if field_limb == 'lower':
        hs -= s.radius
    elif field_limb == 'upper':
        hs += s.radius
    
    # dip / dip short
    h = float(field_eye_height)
    if field_fetch:
        d = float(field_fetch)
        dip = 0.225 * (d / 1000) + 3.435 * h / (d / 1000)
    else:
        dip = 1.76 * math.sqrt(h)
    hs += math.radians(dip / 60.0) 
    
    # format
    hs = math.degrees(hs)
    add = abs(hs)
    d = int(add)
    m = 60 * (add - d)
    minus =  "-" if hs < 0 else ""
    hs = minus + str(d) + "° " + "{:.1f}'".format(m).zfill(5)

# OUTPUT
field_upper_checked = field_lower_checked = field_center_checked = ''
if field_limb == "upper":
    field_upper_checked = "checked"
if field_limb == "lower":
    field_lower_checked = "checked"
if field_limb == "center":
    field_center_checked = "checked"

# set output to utf8
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print("Content-type: text/html")
print("Pragma: no-cache")
print("Cache-Control: no-cache")
print()
# read template
f = io.open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'sextant_height.tpl'), encoding='utf-8')
templ = f.read()
f.close()

# output document
print(templ % {"lat": field_lat, "lon": field_lon, "date": field_date, "time": field_time,
               "upper_checked": field_upper_checked, "lower_checked": field_lower_checked, "center_checked": field_center_checked, 
               "eye_height": field_eye_height, "fetch": field_fetch, "hs": hs})
 
