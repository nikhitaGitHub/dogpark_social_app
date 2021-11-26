function initialize() {
  var map;
  var mapOptions = {
	  zoom: 18,
	  center: new google.maps.LatLng(55.85365783555865, -4.288739944549508)
  };
  var currentLocation = {};
  var rendered = false;
  var mapElm = document.getElementById('map_canvas');
  if(mapElm != null) {
    map = new google.maps.Map(mapElm, 
                mapOptions);
  }
  else {

      function getCookie(name) {
        var cookieValue = null;
        if(document.cookie && document.cookie != "") {
            var cookies = document.cookie.split(';');
            for(i=0; i<cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if(cookie.substring(0, name.length+1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length+1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function getLocation() {
        if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(currentLocationCoordinates);
        }
        else {
            console.log("Geolocation is not supported by this browser.")
        }
    }
    function updatePosition() {
        if(navigator.geolocation) {
            navigator.geolocation.watchPosition(calculateDistance);
        }
        else {
            console.log("Geolocation is not supported by this browser.")
        }
    }
    function currentLocationCoordinates(position) {
        currentLocation.lat = position.coords.latitude;
        currentLocation.lon = position.coords.longitude;
    }

    function calculateDistance(position) {
        var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        var dis = google.maps.geometry.spherical.computeDistanceBetween(pos, mapOptions.center);
        console.log("Update location");
        if(dis <= 1000 && dis >= 0 && rendered == false) {
            console.log("Distance"+dis);
            var url = '/dogpark/';
            var csrftoken = getCookie('csrftoken');
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    in_proximity : 1
                },
                success: function() {
                rendered = true;
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status+": "+xhr.responseText);
                }
            });
        }
        else if(dis > 1000 && rendered == true) {
          var url = '/dogpark/';
          var csrftoken = getCookie('csrftoken');
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    in_proximity: 0
                },
                success: function(json) {
                rendered = false;
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status+": "+xhr.responseText);
                }
            });
        }
    }

    getLocation();
    updatePosition();
  }        
}

function loadTheMap() {
    console.log("In map js");
    var script=document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyC_Ii8L8wy40S8pB-eUBg13MlIOGYHXx6Y&libraries=geometry&callback=initialize';
    document.body.appendChild(script);
};

window.onload = loadTheMap;