#!/usr/bin/env python3

import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os, urllib, codecs, sys, io, base64


# get values into arrays x, y
#data = "\
#11:23:47 36-41\n    \
#11:27:05 36-48\n    \
#11:34:18 37-00\n    \
#11:41:26 37-10\n    \
#11:52:05 37-20\n    \
#11:55:24    37-22\n    \
#12:01:42 37-23\n    \
#12:02:33 37-23\n    \
#12:06:26 37-23\n    \
#12:11:35 37-22  \n    \
#12:14:41 37-20\n    \
#12:20:54 37-16\n    \
#12:31:21 37-03\n    \
#12:38:09 36-52\n    \
#12:43:03 36-42  \
#"

# READ QUERY PARAMETERS

qs = os.environ.get("QUERY_STRING", "")

form_fields = urllib.parse.parse_qs(qs, True)

# SET UP FORM FIELDS (DEFAULTS OR FROM QS)

field_data = form_fields['data'][0] if "data" in form_fields else ''

result = ""
chart = ""

if "submit" in form_fields:
    # processs
    
    x = []
    y = []
    field_data = field_data.strip()
    for l in field_data.splitlines(True):
        sx, sy = l.split()
        h, m, s = sx.split(":")
        vx = float(h) + float(m)/60. + float(s)/3600.
        x.append(vx)
        d, m = sy.split("-")
        vy = float(d) + float(m) / 60.
        y.append(vy)

    # optimize
    def parabola(x, a, b, c):
        return a*x**2 + b*x + c

    def format_time(t, p = None):
        t = float(t)
        h = int(t)
        t = 60 * (t - h)
        m = int(t)
        t = 60 * (t - m)
        s = int(t)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def format_angle(a, p = None):
        a = float(a)
        d = int(a)
        a = 60 * (a -d )
        m = int(a)
        return f"{d:02d}°{m:02d}'"
        

    fit_params, pcov = scipy.optimize.curve_fit(parabola, x, y)

    # get maximum, x of max
    lan_time = scipy.optimize.fmin(lambda x: -(fit_params[0] * x * x + fit_params[1] * x + fit_params[2]), x[0], disp=False)
    lan = fit_params[0] * lan_time * lan_time + fit_params[1] * lan_time + fit_params[2]
 
    result = f"{format_time(lan_time)}, {format_angle(lan)}"

    # print chart with values, save to svn
    xa = np.linspace(x[0], x[-1], 32)
    y_fit = parabola(xa, *fit_params)
    fig, ax = plt.subplots()
    ax.plot(xa, y_fit, label='fit')
    ax.plot(x, y, "r+", label='measurements')
    for i,j in zip(x,y):
        ax.annotate(format_time(i)+","+format_angle(j),xy=(i,j), xytext=(5,5), textcoords='offset points')
    ax.plot(lan_time, lan, "go", label='LAN')
    ax.annotate(format_time(lan_time)+","+format_angle(lan),xy=(lan_time,lan), xytext=(5,5), textcoords='offset points')
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format_time(x,p)))
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format_angle(x,p)))
    ax.legend(loc='lower center')
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    # Embed the result in the html output.
    imgdata = base64.b64encode(buf.getbuffer()).decode("ascii")
    chart =  f"<img src='data:image/png;base64,{imgdata}'/>"

    # return maxY, maxx, chart


# OUTPUT

# set output to utf8
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print("Content-type: text/html")
print("Pragma: no-cache")
print("Cache-Control: no-cache")
print()
# read template
f = io.open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'parabola.tpl'), encoding='utf-8')
templ = f.read()
f.close()

# output document
print(templ % {"data": field_data, "result": result, "chart": chart})
