// Map.js

document.addEventListener("DOMContentLoaded", function() {
    
    // Socket definition
    const socket = io();
    
//    socket.on('disconnect', function() {
//        alert('Connection to the server has been lost.');
//        window.location.href = 'about:blank';
//    });

    // MARK: - Container
    
    const container = document.getElementById("main-container");
    
    let startY;
    let startHeight;
    let momentum;
    let maxHeight;
    const minHeight = 80;
    const elements = container.children;
    
    container.addEventListener("wheel", resize);
    container.addEventListener("touchstart", touchStartResize, false);
    container.addEventListener("touchmove", touchResize, false);
    container.addEventListener("touchend", touchEndResize, false);
    
    function setMaxHeight() {
        maxHeight = 60
        for (let i = 0; i < elements.length; i++) {
            maxHeight += elements[i].offsetHeight;
        }
        
        if (maxHeight < window.innerHeight) {
            if (window.innerWidth > 500) {
                maxHeight = window.innerHeight - 10;
            } else {
                maxHeight = window.innerHeight;
            }
        }
    }
    
    setMaxHeight()
    
    function setRadius() {
        if (container.clientHeight == window.innerHeight) {
            container.style.borderRadius = "0";
        } else {
            container.style.borderTopLeftRadius = "10px";
            container.style.borderTopRightRadius = "10px";
        }
    }
    
    function touchStartResize(e) {
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
    
    function displayInfo(selection) {
        clearMap()
        socket.emit("lookup.all", selection["icao24"], selection["callsign"]);
    }
    
    socket.on('lookup.all', function(info) {
        console.log(info);
        selection = aircraft[info["aircraft"]["ICAO24 address"]];
        selection["marker"].getElement().style.color = "lightgrey";

        try {plotRoute([selection['lat'], selection['lng']],[info["origin"]["Latitude"], info["origin"]["Longitude"]])}
        try {plotRoute([selection['lat'], selection['lng']],[info["destination"]["Latitude"], info["destination"]["Longitude"]])}
    });
    
    // MARK: - Map
    
    function clearMap() {
        map.eachLayer(function(layer) {
            if (layer instanceof L.Polyline) { map.removeLayer(layer) }
        });
        
        Object.keys(aircraft).forEach(function(key) {
            const marker = aircraft[key]['marker'];
            marker.getElement().style.color = ''; // Remove the color style
        });
    }
    
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
    
    function plotRoute(startPoint, endPoint, numPoints = 100) {
        function computeIntermediatePoint(start, end, ratio) {
            const lat1 = start.lat * Math.PI / 180;
            const lon1 = start.lng * Math.PI / 180;
            const lat2 = end.lat * Math.PI / 180;
            const lon2 = end.lng * Math.PI / 180;
            
            const d = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin((lat1 - lat2) / 2), 2) + Math.cos(lat1) * Math.cos(lat2) * Math.pow(Math.sin((lon1 - lon2) / 2), 2)));
            
            const A = Math.sin((1 - ratio) * d) / Math.sin(d);
            const B = Math.sin(ratio * d) / Math.sin(d);
            
            const x = A * Math.cos(lat1) * Math.cos(lon1) + B * Math.cos(lat2) * Math.cos(lon2);
            const y = A * Math.cos(lat1) * Math.sin(lon1) + B * Math.cos(lat2) * Math.sin(lon2);
            const z = A * Math.sin(lat1) + B * Math.sin(lat2);
            
            const lat = Math.atan2(z, Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2))) * 180 / Math.PI;
            const lon = Math.atan2(y, x) * 180 / Math.PI;
            
            return [lat, lon];
        }
        
        const startLatLng = L.latLng(startPoint);
        const endLatLng = L.latLng(endPoint);
        
        const distance = startLatLng.distanceTo(endLatLng);
        
        let curvePoints = [];
        for (let i = 0; i <= numPoints; i++) {
            const ratio = i / numPoints;
            const intermediatePoint = computeIntermediatePoint(startLatLng, endLatLng, ratio);
            curvePoints.push(intermediatePoint);
        }
        
        L.polyline(curvePoints, { color: '#FF9500', weight: 2 }).addTo(map);
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
    
    map.on('click', clearMap)
    
    // Define icons
    let icons = {};
    
    icons["plane"] = L.divIcon({
        className: 'aircraft-icon',
        html: '<div>&#x2708;</div>',
        iconSize: [32, 32]
    });
    
    icons["helicopter"] = L.divIcon({
        className: 'aircraft-icon',
        html: '<div class="helicopter-icon">&#xFF0B;</div>',
        iconSize: [32, 32]
    });
    
    icons["other"] = L.divIcon({
        className: 'aircraft-icon',
        html: '<div>&#x27A4;</div>',
        iconSize: [32, 32]
    });
    
    // MARK: Aircraft
    let aircraft = {};
    
    socket.on('decoder.get', function(payload) {
        oldAircraft = { ...aircraft };
        aircraft = {
            ...aircraft,
            ...payload
        };

        // Add aircraft
        for (const key in aircraft) {
            const individual = aircraft[key];
            
            // Add to map
            
            if (typeof oldAircraft[key] === 'undefined') {
                individual['marker'] = L.marker([individual['lat'], individual['lng']], {
                    icon: icons[individual['icon']],
                }).addTo(map);

                individual['marker'].getElement().classList.add(`_${individual['icao24']}`);
                
            } else {
                setCoordinates(individual, [individual['lat'], individual['lng']])
            }
            
            if (individual['icon'] !== "helicopter") { setHeading(individual, individual['heading']) }
            
            // Add to list
            let parent = document.getElementById('aircraft-list');
            
            let listItem = document.createElement('div');
            listItem.setAttribute('class', `aircraft-list _${individual['icao24']}`);
            
            if (typeof individual['callsign'] === 'undefined')
            listItem.textContent = individual['callsign'];
            parent.appendChild(listItem);
            setMaxHeight();
            
            const infoTriggers = document.querySelectorAll(`._${individual['icao24']}`);
            infoTriggers.forEach(element => {
                element.addEventListener('click', () => {
                    displayInfo(individual)
                });
            });
        }
    });

});
