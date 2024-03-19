// Map.js

// MARK: Container scrolling
document.addEventListener("DOMContentLoaded", function() {
    const container = document.querySelector(".main-container");
    
    let startY;
    let startHeight;
    let momentum;
    let elements = container.children;
    let maxHeight = 60;
    const minHeight = 80;
    
    container.addEventListener("wheel", resize);
    container.addEventListener("touchstart", touchStartResize, false);
    container.addEventListener("touchmove", touchResize, false);
    container.addEventListener("touchend", touchEndResize, false);
    
    function setMaxHeight() {
        if (window.innerWidth > 500) {
            for (let i = 0; i < elements.length; i++) {
                maxHeight += elements[i].offsetHeight;
            }
            
            if (maxHeight < window.innerHeight) {
                maxHeight = window.innerHeight - 10;
            }
            
        } else {
            maxHeight = window.innerHeight;
        }
    }
    
    function setRadius() {
        if (container.clientHeight == window.innerHeight) {
            container.style.borderRadius = "0";
        } else {
            container.style.borderTopLeftRadius = "10px";
            container.style.borderTopRightRadius = "10px";
        }
    }
    
    function touchStartResize(e) {
        setMaxHeight()
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
        setRadius()
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
        if (container.clientHeight == window.innerHeight) {
            container.style.borderRadius = "0";
        } else {
            container.style.borderTopLeftRadius = "10px";
            container.style.borderTopRightRadius = "10px";
        }
        setRadius()
    }
    
    function resize(e) {
        setMaxHeight()
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
        setRadius()
    }
});

// MARK: - Map

function setHeading(aircraft, heading) {
    const marker = aircraft['marker']
    const markerElement = marker.getElement();
    const markerElementInner = markerElement.querySelector("div");
    heading = heading - 90
    markerElementInner.style.transition = "transform 0.5s ease";
    markerElementInner.style.transform = "rotate(" + heading + "deg)";
}

function setCoordinates(aircraft, endPoint) {
    const marker = aircraft['marker']
    const markerLocation = marker.getLatLng();
    const startPoint = [markerLocation.lat, markerLocation.lng];
    
    const numSteps = 60;
    const stepDuration = 250 / numSteps; // animation duration / steps
    const latStep = (endPoint[0] - startPoint[0]) / numSteps;
    const lngStep = (endPoint[1] - startPoint[1]) / numSteps;
    
    let step = 0;
    const markerAnimation = setInterval(function() {
        if (step < numSteps) {
            let newLat = startPoint[0] + (latStep * step);
            let newLng = startPoint[1] + (lngStep * step);
            marker.setLatLng([newLat, newLng]);
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

const plane = L.divIcon({
    className: 'aircraft-icon',
    html: '<div>&#x2708;</div>',
    iconSize: [32, 32],
});

const helicopter = L.divIcon({
    className: 'aircraft-icon',
    html: '<div class="helicopter-icon">&#xFF0B;</div>',
    iconSize: [32, 32],
});

let map = L.map('map', {
    maxZoom: 15,
    zoomControl: false,
    attributionControl: false,
}).setView([51.505, -0.09], 11);

let tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png').addTo(map);

// MARK: Aircraft
let aircraft = {};

// Add demos
aircraft['icao-code-of-an-aeroplane'] = {
    'lat': 51.5,
    'lng': -0.3,
    'heading': 245,
    'icon': plane,
    'icao24': 'icao-code-of-an-aeroplane',
    // etc
};

aircraft['icao-code-of-another-aeroplane'] = {
    'lat': 51.4,
    'lng': -0.2,
    'heading': 45,
    'icon': plane,
    'icao24': 'icao-code-of-another-aeroplane',
};

aircraft['icao-code-of-a-helicopter'] = {
    'lat': 51.6,
    'lng': -0.1,
    'heading': 90,
    'icon': helicopter,
    'icao24': 'icao-code-of-a-helicopter',
};

// Add aircraft to map
for (let key in aircraft) {
    let each = aircraft[key];
    
    each['marker'] = L.marker([each['lat'], each['lng']], {
        icon: each['icon'],
        id: each['icao24']
    }).addTo(map);
    
    if (each['icon'] !== helicopter) { setHeading(each, each['heading']) }
}
