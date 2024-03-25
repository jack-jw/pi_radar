// Map.js

document.addEventListener("DOMContentLoaded", function() {
    
    // Socket definition
    const socket = io();
    
    socket.on('disconnect', function() {
        alert('Connection to the server has been lost.');
        window.location.href = 'about:blank';
    });

    // MARK: - Container
    
    const container = document.getElementById("main-container");
    
    let startY;
    let startHeight;
    let momentum;
    let maxHeight;
    const minHeight = 80;
    
    container.addEventListener("wheel", resize);
    container.addEventListener("touchstart", touchStartResize, false);
    container.addEventListener("touchmove", touchResize, false);
    container.addEventListener("touchend", touchEndResize, false);
    
    function setMaxHeight() {
        const elements = container.children;
        maxHeight = 60
        for (let i = 0; i < elements.length; i++) {
            if (window.getComputedStyle(elements[i]).display !== 'none') {
                maxHeight += elements[i].offsetHeight;
            }
        }
        
        if (maxHeight < window.innerHeight) {
            if (window.innerWidth > 500) {
                maxHeight = window.innerHeight - 10;
            } else {
                maxHeight = window.innerHeight;
            }
        }
        if (window.getComputedStyle(container).height > maxHeight) {
            container.style.height = maxHeight + "px";
        }
    }
    
    window.addEventListener('resize', setMaxHeight);
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
        container.style.transition = null;
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
        container.style.transition = null;
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
    
    function clearMap() {
        map.eachLayer(function(layer) {
            if (layer instanceof L.Polyline) { map.removeLayer(layer) }
        });
        
        Object.keys(aircraft).forEach(function(key) {
            const marker = aircraft[key]['marker'];
            marker.getElement().style.color = '';
        });
        
        document.getElementById('main-container-main-view').style.display = null;
        document.getElementById('main-container-aircraft-view').style.display = "none";
        document.getElementById('main-container-aircraft-view').innerHTML = null;
        setMaxHeight();
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
    
    function plotRoute(startPoint, endPoint, opacity) {
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
        
        let curvePoints = [];
        let oldIntermediatePoint;
        for (let i = 0; i <= 100; i++) {
            const ratio = i / 100; // 100 above and here is point count
            const intermediatePoint = computeIntermediatePoint(startLatLng, endLatLng, ratio);
            curvePoints.push(intermediatePoint);
        }
        
        L.polyline(curvePoints, { color: '#FF9500', weight: 2, opacity: opacity }).addTo(map);
        
        return startLatLng.distanceTo(endLatLng);
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
    
    map.on('click', function() {
        clearMap()
        if (window.innerWidth <= 500) {
            container.style.transition = 'height 0.3s ease';
            container.style.height = minHeight + "px";
        }
    });
    
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
            
            if (typeof individual['callsign'] === 'undefined') {}
            
            let parent = document.getElementById('aircraft-list');
            
            let listItem = document.createElement('div');
            listItem.setAttribute('class', `aircraft-list _${individual['icao24']}`);
            listItem.innerHTML = `
                <h3>${individual['callsign']}</h3>
                <p>${individual['speed']} KTS, ${individual['altitude']} FT, ${individual['heading']}º</p>`;
            
            parent.appendChild(listItem);
            setMaxHeight();
            
            const infoTriggers = document.querySelectorAll(`._${individual['icao24']}`);
            infoTriggers.forEach(element => {
                element.addEventListener('click', () => {
                    socket.emit("lookup.all", individual["icao24"], individual["callsign"]);
                });
            });
        }
    });
    
    socket.on('lookup.all', function(info) {
        socket.emit('jetphotos.thumb',info['aircraft']['Registration'])
        console.log(info);
        selection = aircraft[info["aircraft"]["ICAO24 address"]];
        selection["marker"].getElement().style.color = "lightgrey";
        document.getElementById('main-container-main-view').style.display = 'none';
        aircraftView = document.getElementById('main-container-aircraft-view')
        aircraftView.style.display = null;
        
        let routePercentage;
        try {
            const fromOrigin = plotRoute([selection['lat'], selection['lng']],[info["origin"]["Latitude"], info["origin"]["Longitude"]], 1);
            routePercentage = fromOrigin;
        } catch {
            routePercentage = 0;
        }
        
        try {
            const toDestination = plotRoute([selection['lat'], selection['lng']],[info["destination"]["Latitude"], info["destination"]["Longitude"]], 0.5);
            routePercentage = routePercentage / (routePercentage + toDestination);
        } catch {
            routePercentage = 0;
        }
        
        // Fix this mess
        if (info['origin'] === null) {
            info['origin'] = {};
            info['origin']['IATA code'] = '<input id="origin-input" class="iata-input" style="float: left" contenteditable="true" required maxlength="3" minlength="3">';
            info['origin']['Municipality'] = 'Origin'
        }
        
        if (info['destination'] === null) {
            info['destination'] = {};
            info['destination']['IATA code'] = '<input id="destination-input" class="iata-input" style="text-align: right; float: right" contenteditable="true" required maxlength="3" minlength="3">';
            info['destination']['Municipality'] = 'Destination'
        }
        
        if (info['airline'] == null) {
            info['airline'] = {};
            info['airline']['Airline'] = "Unknown Airline"
        }
        
        aircraftView.innerHTML = `
            <img class="aircraft-img" id="img-${info['aircraft']['Registration']}">
            <div class="aircraft-info">
                
                <div style="position: relative; top: 0; padding: 25px 0">
                    <span style="position: absolute; left: 0" id="back">&larr; ${info['airline']['Airline']}</span>
                    <span style="position: absolute; right: 0">${info['callsign']}</span>
                </div>
                <hr>
                <div style="position: relative; opacity: 0.5; padding: 10px 0">
                    <span style="position: absolute; left: 0">${info['origin']['Municipality']}</span>

                    <span style="position: absolute; right: 0">${info['destination']['Municipality']}</span>
                </div>
                
                <div style="position: relative; margin: 0; padding-bottom: 50px">
                    <h1 style="position: absolute; left: 0">${info['origin']['IATA code']}</h1>
                    
                    <h1 style="position: absolute; right: 0">${info['destination']['IATA code']}</h1>
                    
                    <h1 style="position: absolute; left: 50%; transform: translateX(-50%)">&#x2708;</h1>
                </div>
                <progress style="width: 100%; position: relative" value="${routePercentage}" max="1"></progress>
            </div>
        `;
        
        
        let latlng = selection['marker'].getLatLng();
        let point = map.latLngToContainerPoint(latlng);
        let xOffset = 0;
        let yOffset = 0;

        container.style.transition = 'height 0.3s ease';
        if (window.innerWidth > 500) {
            container.style.height = (window.innerHeight - 10) + "px";
            xOffset = -160
        } else {
            container.style.height = "350px";
            yOffset = 220
        }
        point.x += xOffset;
        point.y += yOffset;
        map.panTo(map.containerPointToLatLng(point));
        
        setMaxHeight()
        document.getElementById('back').addEventListener('click', clearMap);
    });
    
    socket.on('jetphotos.thumb', function(image) {
        imageId = 'img-' + image['tail']
        try {document.getElementById(imageId).src = image["url"]} catch {}
    });
});
