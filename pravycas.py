#!/usr/bin/python3
# coding=utf-8

from __future__ import print_function
import ephem, datetime, sys, math, os, io, codecs, pygeoip, pickle, cgi, binascii, geocoder

try:
    from http.cookies import SimpleCookie
except ImportError:
    from Cookie import SimpleCookie

COOKIE_NAME = "pravycas_location"
    
def same_time(d1, d2, diff = ephem.minute / 2):
    d1l = d1 - diff
    d1h = d1 + diff
    d2l = d2 - diff
    d2h = d2 + diff
    if (d1l <= d2h and d1h >= d2h) or (d1l <= d2l and d1h > d2l):
        return True
        
def format_ZA_hours_minutes(d1, d2):
    d = abs(d2 - d1)
    h = int(math.floor(d / ephem.hour))
    m = int(math.floor(d % ephem.hour / ephem.minute))
    s = "Za "
    if h > 0:
        s += "<em>"+str(h)+"</em> "
        if h == 1:
            s += "hodinu"
        elif 1 < h < 5:
            s += "hodiny"
        else:
            s += "hodin"
        if m > 0:
            s += " a "
    if m > 0:
        s += "<em>"+str(m)+"</em> "
        if m == 1:
            s += "minutu"
        elif 1 < m < 5:
            s += "minuty"
        else:
            s += "minut"
    if h == 0 and m == 0:
        s = "Právě teď"
    return s

def local_solar_time(loc, d):
    d = ephem.date(datetime.datetime.utcnow())
    pnoon = loc.previous_transit(ephem.Sun())
    noon = loc.next_transit(ephem.Sun())

    e12h = ephem.hours("12:00")
    return ephem.hours(2 * e12h * (d-pnoon) / (noon - pnoon) + e12h ).norm

def format_time(loc, d):
    s = ephem.Sun()
    # get sunrise, sunset, transit
    sunrise = loc.next_rising(s, start = d - ephem.minute)
    noon = loc.next_transit(s, start = d - ephem.minute)
    sunset = loc.next_setting(s, start = d - ephem.minute)

    if same_time(sunrise, d):
        time_str = "Právě vychází slunce."
    elif same_time(noon, d):
        time_str = "Je právě    poledne."
    elif same_time(sunset, d):    
        time_str = "Právě zapadá slunce."
    elif sunrise < noon and sunrise < sunset: # night
        time_str = format_ZA_hours_minutes(d, sunrise) + " vyjde slunce."
    elif noon < sunrise and noon < sunset: # am
        time_str = format_ZA_hours_minutes(d, noon) + " bude poledne."
    elif sunset < noon and sunset < sunrise: #pm
        time_str = format_ZA_hours_minutes(d, sunset) + " zapadne slunce."
    
    return time_str
    
def format_weekday(wd):
    wds = ("pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")
    return "Je " + wds[int(wd)] + "."
    
def format_moon(d):
    #get moon age
    pnm = ephem.previous_new_moon(d)
    age = int(math.floor(abs(pnm - d)))
    s = "Měsíc je "
    if age == 0:
        s += "v novu."
    else:
        s += "<em>"+str(age)+"</em> "
        if age == 1:
            s += "den"
        elif age < 5:
            s += "dny"
        else:
            s += "dnů"
        s += " starý, "
        # find out if moon is within a day of previous event
        if abs(d - ephem.previous_first_quarter_moon(d)) < 1:
            s += "je v první čtvrti."
        elif abs(d - ephem.previous_full_moon(d)) < 1:
            s += "je úplněk."
        elif abs(d - ephem.previous_last_quarter_moon(d)) < 1:
            s += "je v třetí čtvrti."
        else:
            # else add phase it is growing into
            diff = abs(d - ephem.next_new_moon(d))
            sp = "couvá do novu."
            diff1 = abs(d - ephem.next_full_moon(d))
            if diff1 < diff:
                diff = diff1
                sp = "dorůstá do úplňku."
            diff1 = abs(d - ephem.next_first_quarter_moon(d))
            if diff1 < diff:
                diff = diff1
                sp = "dorůstá k první čtvrti."
            diff1 = abs(d - ephem.next_last_quarter_moon(d))
            if diff1 < diff:
                diff = diff1
                sp = "couvá k třetí čtvrti."
            s += sp    
            
    return s
    
def format_PRED_days_hours(diff):
    s = "před "
    if diff > 1:
        days = int(math.floor(diff))
        s += "<em>" + str(days) + "</em> "
        if days == 1:
            s+= " dnem"
        else:
            s+= " dny"
    else:
        hours = int(math.floor(diff / ephem.hour))
        if hours == 0:
            s += "méně než hodinou"
        else:
            s += "<em>" + str(hours) + "</em> "
            if hours == 1:
                s += "hodinou"
            else:
                s += "hodinami"
    return s

def format_ZA_days_hours(diff):
    s = "za "
    if diff > 1:
        days = int(math.floor(diff))
        s += "<em>" + str(days) + "</em> "
        if days == 1:
            s += "den"
        elif days < 5:
            s += "dny"
        else:
            s += "dnů"
    else:
        hours = int(math.floor(diff / ephem.hour))
        if hours == 0:
            s += "méně než hodinu"
        else:
            s += "<em>" + str(hours) + "</em> "
            if hours == 1:
                s += "hodinu"
            elif hours < 5:
                s += "hodiny"
            else:
                s += "hodin"
    return s
    
def format_season(d):
    s = ephem.Sun()
    # check if an event occured recently
    diff_limit = 15
    ps = ephem.previous_solstice(d)
    diff = abs(ps - d)
    if diff < diff_limit:
        sh = format_PRED_days_hours(diff)
        if ps.tuple()[1] == 6:
            # summer solstice
            s = "Je léto, " + sh + " byl letní slunovrat."
        else:
            # winter solstice
            s = "Je zima, " + sh + " byl zimní slunovrat."
    else:
        pe = ephem.previous_equinox(d)
        diff = abs(ephem.previous_equinox(d) - d)
        if diff < diff_limit:
            sh = format_PRED_days_hours(diff)
            if pe.tuple()[1] == 3:
                # spring equinox
                s = "Je jaro, " + sh + " byla jarní rovnodennost."
            else:
                # fall equinox
                s = "Je podzim, " + sh + " byla podzimní rovnodennost."
        else:
            # count days and hours to next event
            ns = ephem.next_solstice(d)
            diff = abs(ns - d)
            sh = format_ZA_days_hours(diff)
            if ns.tuple()[1] ==  6:
                # summer solstice
                s = "Je jaro, " + sh + " bude letní slunovrat."
            else:
                # winter solstice
                s = "Je podzim, " + sh + " bude zimní slunovrat."       
            
            ne = ephem.next_equinox(d)
            diff1 = abs(ne - d)
            if diff1 < diff:
                sh = format_ZA_days_hours(diff1)
                if ne.tuple()[1] == 3:
                    # spring equinox
                    s = "Je zima, " + sh + " bude jarní rovnodennost."
                else:
                    # fall equinox
                    s = "Je léto, " + sh + " bude podzimní rovnodennost."
    
    return s

# check if called with position arguments
form = cgi.FieldStorage()
if "lat" in form and "lon" in form:
    lat = form['lat'].value
    lon = form['lon'].value
    if 'txt' in form:
        txt = form['txt'].value
    else:
        try:
            g = geocoder.google([float(lat), float(lon)], method='reverse')
            txt = g.city + ", " + g.country
        except:
            txt = "%.3f" % float(lat) + ", %.3f" % float(lon)
    loc = {
        'txt': txt, 
        'lat': lat,
        'lon': lon
    }
else:
    # get cookie

    try:
        cookies = SimpleCookie(os.environ["HTTP_COOKIE"])
        loc = pickle.loads(binascii.unhexlify(cookies[COOKIE_NAME].value))
        
    except:
        # if no cookie, try to do GeoIP lookup
        try:
            gi = pygeoip.GeoIP(os.path.join(os.path.dirname(os.path.realpath(__file__)),'GeoLiteCity.dat'))
            ip = os.environ["REMOTE_ADDR"]
            qr = gi.record_by_addr(ip)
            if qr['city'] == None and qr['country_name'] == None:
                try:
                    g = geocoder.google([float(qr['latitude']), float(qr['longitude'])], method='reverse')
                    txt = g.city + ", " + g.country
                except:
                    txt = "%.3f" % float(qr['latitude']) + ", %.3f" % float(qr['longitude'])
            elif qr['city'] == None:
                txt = qr['country_name']
            else:
                txt = qr['city'] + ', ' + qr['country_code'] 
            loc = {
                'txt': txt, 
                'lat': qr['latitude'],
                'lon': qr['longitude']
            }
        except:
            loc = {'txt':'neznámé místo', 'lat':0.0, 'lon':0.0}
    
    
# format output

# output, set cookie

expiration = datetime.datetime.now() + datetime.timedelta(days=90)
cookie = SimpleCookie()
cookie[COOKIE_NAME] = binascii.hexlify(pickle.dumps(loc)).decode()
cookie[COOKIE_NAME]["path"] = "/"
cookie[COOKIE_NAME]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S UTC")

# set output to utf8
try:  #python3
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
except: #python2
    reload(sys)
    sys.setdefaultencoding("utf-8")
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

print("Content-type: text/html")
print(cookie.output())
print("Pragma: no-cache")
print("Cache-Control: no-cache")
print()
# read template
f = io.open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'pravycas.tpl'), encoding='utf-8')
templ = f.read()
f.close()

# output document

# location & date
d = ephem.date(datetime.datetime.utcnow())
l = ephem.Observer()
l.lon = str(loc['lon'])
l.lat = str(loc['lat'])
l.date = d

st = str(local_solar_time(l, d))[:-3]

ft = format_time(l, d) + " " + format_weekday(ephem.localtime(d).weekday()) + " " + format_moon(d) + " " + format_season(d)

print(templ % {"misto": loc['txt'], "lst": st, "obsah": ft})
