
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

function calculateDistance(position) {
    var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
    var target = new google.maps.LatLng(55.85365783555865, -4.288739944549508);
    var dis = google.maps.geometry.spherical.computeDistanceBetween(pos, target);
    if(dis <= 1000 && dis >= 0) {
        var url = '/dogpark/near_park/';
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: url,
            type: "POST",
            async: false,
            data: {
                csrfmiddlewaretoken: csrftoken,
                in_proximity : 1
            },
            success: function(data) {
                if(data == 1) {
                    window.location = '/dogpark/render_near_park';
                }
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status+": "+xhr.responseText);
            }
        });
    }
    else if(dis > 1000 ) {
        var url = '/dogpark/near_park/';
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: url,
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrftoken,
                in_proximity: 0
            },
            success: function(data) {
                if(data == 1) {
                    window.location = '/dogpark/';
                }
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status+": "+xhr.responseText);
            }
        });
    }
}

function initialize() {
  var map;
  var currentLocation = {};
  var mapOptions = {
    zoom: 18,
    center: new google.maps.LatLng(55.85365783555865, -4.288739944549508)
  };
  var mapElm = document.getElementById('map_canvas');
  if(mapElm != null) {
    map = new google.maps.Map(mapElm, 
                mapOptions);
  }
  else {
    window.w = navigator.geolocation.watchPosition(calculateDistance);
  }        
}

function loadTheMap() {
    var script=document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyC_Ii8L8wy40S8pB-eUBg13MlIOGYHXx6Y&libraries=geometry&callback=initialize';
    document.body.appendChild(script);
};

window.onload = loadTheMap;