// Map.js

// MARK: Container scrolling
document.addEventListener("DOMContentLoaded", function() {
    const container = document.querySelector(".main-container");
    
    let elements = container.children;
    let maxHeight = 60;
    const minHeight = 80;
    
    for (let i = 0; i < elements.length; i++) {
        maxHeight += elements[i].offsetHeight;
    }
    
    if (maxHeight < window.innerHeight) {
        maxHeight = window.innerHeight * 0.985;
    }
    
    container.addEventListener("wheel", resize);
    container.addEventListener("touchstart", touchStartResize, false);
    container.addEventListener("touchmove", touchResize, false);
    container.addEventListener("touchend", touchEndResize, false);
    
    let startY;
    let startHeight;
    let momentum;
    
    function touchStartResize(e) {
        startY = e.touches[0].clientY;
        startHeight = container.clientHeight;
        momentum = 0;
    }
    
    function touchResize(e) {
        if (!startY) {
            return;
        }
        
        let deltaY = startY - e.touches[0].clientY;
        momentum = deltaY * 0.2; // 0.2 is scroll multiplier
        
        let newHeight = startHeight + deltaY;
        
        if (newHeight >= minHeight && newHeight <= maxHeight) {
            container.style.height = newHeight + "px";
        } else if (newHeight < minHeight) {
            container.style.height = minHeight + "px";
        } else if (newHeight > maxHeight) {
            container.style.height = maxHeight + "px";
        }
        
        e.preventDefault();
    }
    
    function touchEndResize(e) {
        startY = null;
        startHeight = null;
        if (momentum !== 0) {
            let interval = setInterval(function() {
                let newHeight = container.clientHeight + momentum;
                if (newHeight >= minHeight && newHeight <= maxHeight) {
                    container.style.height = newHeight + "px";
                    momentum *= 0.9; // 0.9 is decay rate
                } else {
                    clearInterval(interval);
                }
            }, 32);
        }
    }
    
    function resize(e) {
        let delta = e.deltaY;
        let newHeight = container.clientHeight + delta;
        if (newHeight >= minHeight && newHeight <= maxHeight) {
            container.style.height = newHeight + "px";
        } else if (newHeight < minHeight) {
            container.style.height = minHeight + "px";
        } else if (newHeight > maxHeight) {
            container.style.height = maxHeight + "px";
        }
        e.preventDefault();
    }
});

// MARK: - The map
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
        console.error('Invalid theme name:', themeName);
        return;
    }
    tileLayer.setUrl(tileLayerURL);
}

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

let aircraft = []

let map = L.map('map', {
    maxZoom: 15,
    zoomControl: false,
    attributionControl: false,
}).setView([51.505, -0.09], 11);

let tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png').addTo(map);
setTheme('default')

// Check for location - remove because of lack of https?
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
