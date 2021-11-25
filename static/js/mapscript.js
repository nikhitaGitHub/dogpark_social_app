function initialize() {
  var map;
  var mapOptions = {
	zoom: 18,
	  center: new google.maps.LatLng(55.85365783555865, -4.288739944549508)
  };
  map = new google.maps.Map(document.getElementById('map_canvas'), 
							mapOptions);
}

function loadTheMap() {
    var script=document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyC_Ii8L8wy40S8pB-eUBg13MlIOGYHXx6Y&callback=initialize';
    document.body.appendChild(script);
};

window.onload = loadTheMap;