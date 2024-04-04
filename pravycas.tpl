<!DOCTYPE html>
<html lang='cz'>
<head>
    <meta charset='utf-8'/>
  	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pravý čas</title>
    <script type="text/javascript"
      src="https://maps.googleapis.com/maps/api/js?key=XXXXXX&sensor=false">
    </script>
    <script>
function refreshPage() {
  if (!window.preventRefresh) {
    window.location.assign(window.location.href) 
  }
}


function getLocation()
  {
  if (navigator.geolocation)
    {
    window.preventRefresh = 1
    navigator.geolocation.getCurrentPosition(positionFound, positionNotFound);
    }
  }

function positionFound(position)
  {  
    window.location.assign("?lat=" + position.coords.latitude + "&lon=" + position.coords.longitude)  
  }

function positionNotFound(error)
  {
    window.preventRefresh = 0
  }

google.maps.Map.prototype.markers = new Array();

google.maps.Map.prototype.addMarker = function(marker) {
    this.markers[this.markers.length] = marker;
};

google.maps.Map.prototype.getMarkers = function() {
    return this.markers
};

google.maps.Map.prototype.clearMarkers = function() {
    for(var i=0; i<this.markers.length; i++){
        this.markers[i].setMap(null);
    }
    this.markers = new Array();
};
  
function showConfig() {
  window.preventRefresh = 1

  // show/hide the divs
  var el = document.getElementById("pravycas_display");
  el.style.display = 'none';
  el = document.getElementById("pravycas_config");
  el.style.display = 'inherit';

  // initialize google maps
  if (window.truetimeMap == undefined) {
    var mapOptions = {
      zoom: 4,
      center: new google.maps.LatLng(46,6)
    };
    var map = new google.maps.Map(document.getElementById('pravycas_map'),
        mapOptions);
    google.maps.event.addListener(map, 'click', function(e) {
      mapClicked(e.latLng, map);
    });
  }
}

function mapClicked(position, map) {
  // show on the map
  map.clearMarkers();
  var marker = new google.maps.Marker({
    position: position,
    map: map
  });
  map.addMarker(marker);
  map.panTo(position);
  // fill text fields
  var elLat = document.getElementById('elLat');
  var elLon = document.getElementById('elLon');
  elLat.value = position.lat();
  elLon.value = position.lng();
}

function hideConfig() {
  window.preventRefresh = 0
  // show/hide the divs
  var el = document.getElementById("pravycas_display");
  el.style.display = 'inherit';
  el = document.getElementById("pravycas_config");
  el.style.display = 'none';
}

function setPosition() {
  var lat = parseFloat(document.getElementById('elLat').value);
  var lon = parseFloat(document.getElementById('elLon').value);
  if (!isNaN(lat) && !isNaN(lon)) {
    hideConfig();
    window.location.assign("?lat=" + lat + "&lon=" + lon)  
  }
}  

function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

function tickClock() {
  // get time
  el = document.getElementById("lst");
  str = el.innerHTML.trim()
  // convert to numbers
  r = str.match(/(\d+):(\d+):(\d+)/);
  h = parseInt(r[1]);
  m = parseInt(r[2]);
  s = parseInt(r[3]);
  // add second
  ps = (s + 1) / 60 >> 0;
  s = (s + 1) %% 60;
  pm = (m + ps) / 60 >> 0;
  m = (m + ps) %% 60;
  h = (h + pm) %% 24 >> 0;
  // update
  el.innerHTML = h.toString() + ":" + pad(m.toString(),2) + ":" + pad(s.toString(),2);
}

function setTimers() {
  setInterval(refreshPage, 60*1000);
  setInterval(tickClock, 1*1000);
}

    </script>
    <style>
        #pravycas {
            font-family: sans-serif;
        }
	#pravycas h1 {
	    margin-top: 0;
	    font-size: large;
	}
        #pravycas a{
            color: #ff6600;
        }
        #pravycas em {
            font-weight: bold;
            color: #ff6600;
        }
        #pravycas footer {
            font-size: small;
        }
        #pravycas #lst { 
            margin:0;
            font: bold xx-large monospace;
        }
    </style>
</head>
<body onload="setTimers()">
<div id='pravycas'>
    <div id="pravycas_display">
        <h1>Pravý čas</h1>
        <p id="lst">
            %(lst)s
        </p>
        <p>
            %(obsah)s
        </p>
        <footer>
            <p>
                Místo: %(misto)s | <a href='javascript:getLocation();'>Zjistit polohu</a> | <a href='javascript:showConfig();'>Nastavit polohu</a> <!-- | <a href=''>Více informací</a> -->
            </p>
        </footer>
    </div>
    <div id="pravycas_config" style="display:none;">
      <div id="pravycas_map" style="width:100%%;height:400px"></div>
      <div>Šířka:<input id="elLat">Délka:<input id="elLon"></div>
      <div><button onclick="setPosition();">Nastavit pozici</button><button id="configCancel" onclick="hideConfig();">Zrušit</button></div>
</div>
</body>
</html>
