// Map.js

document.addEventListener("DOMContentLoaded", function() {
    
    // Socket definition
    const socket = io();

    // MARK: Container scrolling
    const container = document.querySelector(".main-container");
    
    let startY;
    let startHeight;
    let momentum;
    let maxHeight = 60;
    const minHeight = 80;
    const elements = container.children;
    
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
        
        const deltaY = startY - e.touches[0].clientY;
        momentum = deltaY * 0.2; // 0.2 is scroll multiplier
        
        const newHeight = startHeight + deltaY;
        
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
            const interval = setInterval(function() {
                const newHeight = container.clientHeight + momentum;
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
    
    const map = L.map('map', {
    maxZoom: 15,
    zoomControl: false,
    attributionControl: false,
    }).setView([51.505, -0.09], 11);
    
    const tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png').addTo(map);
    
    const plane = L.divIcon({
    className: 'aircraft-icon',
    html: '<div>&#x2708;</div>',
    iconSize: [32, 32]
    });
    
    const helicopter = L.divIcon({
    className: 'aircraft-icon',
    html: '<div class="helicopter-icon">&#xFF0B;</div>',
    iconSize: [32, 32]
    });
    
    const other = L.divIcon({
    className: 'aircraft-icon',
    html: '<div>&#x27A4;</div>',
    iconSize: [32, 32]
    });
    
    // MARK: Aircraft
    let aircraft = {};
    
    // Add demos
    aircraft['aeroplane1'] = {
        'lat': 51.5,
        'lng': -0.3,
        'heading': 70,
        'altitude': 2000,
        'xspeed': 300,
        'yspeed': 10,
        'icon': plane,
        'icao24': 'aeroplane1',
        'callsign': 'BAW15'
    };
    
    aircraft['aeroplane2'] = {
        'lat': 51.4,
        'lng': -0.2,
        'heading': 350,
        'altitude': 1500,
        'xspeed': 200,
        'yspeed': -10,
        'icon': plane,
        'icao24': 'aeroplane2',
        'callsign': 'QFA2'
    };
    
    aircraft['helicopter'] = {
        'lat': 51.6,
        'lng': -0.1,
        'heading': 90,
        'altitude': 500,
        'xspeed': 30,
        'yspeed': 5,
        'icon': helicopter,
        'icao24': 'helicopter',
    };
    
    aircraft['ufo'] = {
        'lat': 51.55,
        'lng': 0,
        'heading': 30,
        'icon': other,
        'icao24': 'ufo',
    };
    // End demos
    
    // Load actual planes
    //socket.on('aircraft', function(payload) {
    //    aircraft = {
    //        ...aircraft
    //        ...payload
    //    }
    //});
    
    
    // Add aircraft to map
    for (let key in aircraft) {
        const each = aircraft[key];
        
        each['marker'] = L.marker([each['lat'], each['lng']], {
        icon: each['icon'],
        id: each['icao24']
        }).addTo(map);
        
        if (each['icon'] !== helicopter) { setHeading(each, each['heading']) }
    }
});
