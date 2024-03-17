// Map.js

function setHeading(aircraft, heading) {
    let aircraftElement = aircraft.getElement();
    let aircraftElementInner = aircraftElement.querySelector("div");
    heading = heading - 90
    aircraftElementInner.style.transition = "transform 0.5s ease";
    aircraftElementInner.style.transform = "rotate(" + heading + "deg)";
    setTimeout(() => {}, 5000);
}

function setCoordinates(aircraft, endPoint) {
    let aircraftLocation = aircraft.getLatLng();
    let startPoint = [aircraftLocation.lat, aircraftLocation.lng];
    
    let numSteps = 60;
    let stepDuration = 250 / numSteps; // animation duration / steps
    let latStep = (endPoint[0] - startPoint[0]) / numSteps;
    let lngStep = (endPoint[1] - startPoint[1]) / numSteps;
    
    let step = 0;
    let markerAnimation = setInterval(function() {
        if (step < numSteps) {
            let newLat = startPoint[0] + (latStep * step);
            let newLng = startPoint[1] + (lngStep * step);
            aircraft.setLatLng([newLat, newLng]);
            step++;
        } else {
            clearInterval(markerAnimation);
        }
    }, stepDuration);
}

function setTheme(themeName) {
    let tileLayerURL;
    if (themeName === 'default') {
        tileLayerURL = 'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png';
    } else if (themeName === 'OSM') {
        tileLayerURL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    } else if (themeName === 'watercolour') {
        tileLayerURL = 'https://watercolormaps.collection.cooperhewitt.org/tile/watercolor/{z}/{x}/{y}.jpg';
    } else {
        // Handle the case when themeName doesn't match any predefined themes
        console.error('Invalid theme name:', themeName);
        return;
    }
    tileLayer.setUrl(tileLayerURL);
}

let aircraft = []

//L.Browser.retina = true;

let map = L.map('map', {
	maxZoom: 15,
	zoomControl: false,
	attributionControl: false,
}).setView([51.505, -0.09], 11);

let tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png').addTo(map);
setTheme('default')

const planeIcon = L.divIcon({
    className: 'aircraft-icon',
    html: '<div>&#x2708;</div>',
    iconSize: [32, 32],
});

const helicopterIcon = L.divIcon({
    className: 'aircraft-icon',
    html: '<div class="helicopter-icon">&#xFF0B;</div>',
    iconSize: [32, 32],
});

const currentLocationIcon = L.divIcon({
    className: 'current-location-icon',
    html: '<div class="current-location-icon-inner"></div>',
    iconSize: [22, 22]
});

aircraft.push(L.marker([51.5, -0.09], {
    id: '40779a',
    icon: planeIcon
}).addTo(map));

aircraft.push(L.marker([51.6, -0.1], {
    id: 'copter',
    icon: helicopterIcon
}).addTo(map));

setHeading(aircraft[0],270)

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        let userLat = position.coords.latitude;
        let userLng = position.coords.longitude;
        map.setView([userLat, userLng], 11);
        L.marker([userLat, userLng], {icon: currentLocationIcon}).addTo(map)
        
        document.addEventListener('keydown', function(event) {
            if (event.metaKey && event.keyCode === 75) {
                map.setView([userLat, userLng], 11);
            }
        });
    });
}
