// Piradar
// Map.js

document.addEventListener("DOMContentLoaded", function() {
    let startContainerY, startContainerHeight, containerMomentum, maxContainerHeight, info, polylines;
    let selection = null;

    const socket = io();
    socket.on('disconnect', function() {
        location.reload()
    });

    // MARK: - Container

    const container = document.getElementById("main-container");
    const minContainerHeight = 80;

    container.addEventListener("wheel", resizeContainer);
    container.addEventListener("touchstart", touchStartResizeContainer);
    container.addEventListener("touchmove", touchResizeContainer);
    container.addEventListener("touchend", touchEndResizeContainer);

    function setMaxContainerHeight() {
        const elements = container.children;
        maxContainerHeight = 60
        for (let i = 0; i < elements.length; i++) {
            if (window.getComputedStyle(elements[i]).display !== 'none') {
                maxContainerHeight += elements[i].offsetHeight;
            }
        }

        if (maxContainerHeight < window.innerHeight) {
            if (window.innerWidth > 500) {
                maxContainerHeight = window.innerHeight - 10;
            } else {
                maxContainerHeight = window.innerHeight;
            }
        }

        if (window.getComputedStyle(container).height > maxContainerHeight) {
            container.style.height = maxContainerHeight + "px";
        }
    }

    window.addEventListener('resize', setMaxContainerHeight);
    setMaxContainerHeight();

    function setContainerRadius() {
        if (container.clientHeight >= window.innerHeight) {
            container.style.borderRadius = "0";
        } else {
            container.style.borderTopLeftRadius = "10px";
            container.style.borderTopRightRadius = "10px";
        }
    }

    function resizeContainer(e) {
        console.log(e.deltaY)
        container.style.transition = null;
        const newHeight = container.clientHeight + e.deltaY;
        if (newHeight >= minContainerHeight && newHeight <= maxContainerHeight) {
            container.style.height = newHeight + "px";
        } else if (newHeight < minContainerHeight) {
            container.style.height = minContainerHeight + "px";
        } else if (newHeight > maxContainerHeight) {
            container.style.height = maxContainerHeight + "px";
        }
        e.preventDefault();
        setContainerRadius();
    }

    function touchStartResizeContainer(e) {
        container.style.transition = null;
        startY = e.touches[0].clientY;
        startHeight = container.clientHeight;
        containerMomentum = 0;
    }
    function touchResizeContainer(e) {
        if (!startY) {
            return;
        }
        const changeInY = startY - e.touches[0].clientY;
        containerMomentum = changeInY * 0.2; // 0.2 is scroll multiplier
        const newHeight = startHeight + changeInY;
        if (newHeight >= minContainerHeight && newHeight <= maxContainerHeight) {
            container.style.height = newHeight + "px";
        } else if (newHeight < minContainerHeight) {
            container.style.height = minContainerHeight + "px";
        } else if (newHeight > maxContainerHeight) {
            container.style.height = maxContainerHeight + "px";
        }
        e.preventDefault();
        setContainerRadius();
    }

    function touchEndResizeContainer() {
        startY = startHeight = null;
        if (containerMomentum !== 0) {
            const interval = setInterval(function() {
                const newHeight = container.clientHeight + containerMomentum;
                if (newHeight >= minContainerHeight && newHeight <= maxContainerHeight) {
                    container.style.height = newHeight + "px";
                    containerMomentum *= 0.9; // 0.9 is decay rate
                } else {
                    clearInterval(interval);
                }
            }, 32);
        }
        setContainerRadius()
    }

    // MARK: - Map

    function clearMap() {
        map.eachLayer(function(layer) {
            if (layer instanceof L.Polyline) { map.removeLayer(layer) }
        });
        
        Object.keys(aircraft).forEach(function(key) {
            const marker = aircraft[key].marker;
            marker.getElement().style.color = '';
        });
        
        document.getElementById('main-container-main-view').style.display = null;
        document.getElementById('main-container-aircraft-view').style.display = "none";
        document.getElementById('main-container-aircraft-view').innerHTML = null;
        selection = info = polylines = null;
        setMaxContainerHeight();
    }

    function setAircraft(anAircraft) {
        const marker = anAircraft.marker;

        if (anAircraft.icon !== "helicopter") {
            const iconHeading = anAircraft.hdg - 90;
            const markerElement = marker.getElement();
            const markerElementInner = markerElement.querySelector("div");
            markerElementInner.style.transition = "transform 0.5s ease";
            markerElementInner.style.transform = "rotate(" + iconHeading + "deg)";
        }

        const speed = anAircraft.speed / (1.944 * 100);
        if (marker.moveInterval) {
            clearInterval(marker.moveInterval);
        }

        const radianAngle = anAircraft.hdg * (Math.PI / 180);

        function fly() {
            const changeInLat = Math.cos(radianAngle) * (speed / 111111);
            const changeInLng = Math.sin(radianAngle) * (speed / (111111 * Math.cos(marker.getLatLng().lat * (Math.PI / 180))));
            const currentLatLng = marker.getLatLng();
            const newLatLng = {
                lat: currentLatLng.lat + changeInLat,
                lng: currentLatLng.lng + changeInLng
            };
            marker.setLatLng(newLatLng);
            if (selection !== null) {
                if (selection.icao24 === polylines.icao24) {
                    plotRoutes();
                }
            }
        }

        marker.moveInterval = setInterval(fly, 10);
    }

    function plotGreatCircleRoute(startPoint, endPoint, opacity) {
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
        for (let i = 0; i <= 100; i++) {
            const ratio = i / 100;
            const intermediatePoint = computeIntermediatePoint(startLatLng, endLatLng, ratio);
            curvePoints.push(intermediatePoint);
        }

        const line = L.polyline(curvePoints, { color: '#FF9500', weight: 2, opacity: opacity }).addTo(map);
        const distance = startLatLng.distanceTo(endLatLng); // need to implement great circle distance calc

        return {'line': line, 'distance': distance}
    }

    function plotRoutes() {
        try { map.removeLayer(polylines.origin.line); } catch {}
        try { map.removeLayer(polylines.destination.line); } catch {}

        let fromOrigin, toDestination;
        let percentage = 0;
        if (info.origin.muni !== 'Origin') {
            fromOrigin = plotGreatCircleRoute([info.origin.lat, info.origin.lng], selection.marker.getLatLng(), 1)
        }
        if (info.destination.muni !== 'Destination') {
            toDestination = plotGreatCircleRoute(selection.marker.getLatLng(), [info.destination.lat, info.destination.lng], 0.5)
        } if (info.origin.muni !== 'Origin' && info.destination.muni !== 'Destination') {
            percentage = fromOrigin.distance / (fromOrigin.distance + toDestination.distance)
        }

        polylines = {'origin': fromOrigin, 'destination': toDestination, 'percentage': percentage, 'icao24': selection.icao24}
    }
    
    function setTheme(themeName) {
        let tileLayerURL;
        if (themeName === 'default') {
            tileLayerURL = 'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png';
            document.querySelector('.leaflet-tile-pane').style.filter = '';
        } else if (themeName === 'OSM') {
            tileLayerURL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
            document.querySelector('.leaflet-tile-pane').style.filter = '';
        } else if (themeName === 'watercolour') {
            tileLayerURL = 'https://watercolormaps.collection.cooperhewitt.org/tile/watercolor/{z}/{x}/{y}.jpg';
            document.querySelector('.leaflet-tile-pane').style.filter = 'none';
        } else if (themeName === 'satellite') {
            tileLayerURL = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
            document.querySelector('.leaflet-tile-pane').style.filter = 'none';
        } else { return; }
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

    icons.plane = L.divIcon({
        className: 'aircraft-icon',
        html: '<div>&#x2708;</div>',
        iconSize: [32, 32]
    });

    icons.helicopter = L.divIcon({
        className: 'aircraft-icon',
        html: '<div class="helicopter-icon">&#xFF0B;</div>',
        iconSize: [32, 32]
    });

    icons.other = L.divIcon({
        className: 'aircraft-icon',
        html: '<div>&#x27A4;</div>',
        iconSize: [32, 32]
    });

    // MARK: - Aircraft
    let aircraft = {};

    socket.on('decoder.get', function(payload) {
        oldAircraft = { ...aircraft };
        aircraft = {
            ...aircraft,
            ...payload
        };

        for (const key in aircraft) {
            const individual = aircraft[key];

            if (typeof oldAircraft[key] === 'undefined') {
                individual.marker = L.marker([individual.lat, individual.lng], {
                    icon: icons[individual.icon],
                    className: `_${individual.id}`
                }).addTo(map);
            }

            setAircraft(individual)

            let listParent = document.getElementById('aircraft-list');
            let listItem = document.createElement('div');
            listItem.setAttribute('class', `aircraft-list _${individual.icao24}`);
            listItem.innerHTML = `
                <h3>${individual.callsign}</h3>
                <p>${individual.callsign} KTS, ${individual.alt} FT, ${individual.hdg}º</p>`;

            listParent.appendChild(listItem);
            setMaxContainerHeight();

            document.querySelectorAll(`._${individual.icao24}`).forEach(element => {
                element.addEventListener('click', function(e) {
                    socket.emit("lookup.all", individual.icao24, individual.callsign);
                });
            });

        }
    });

    socket.on('lookup.all', function(response) {
        info = response;

        if (info.origin === null) {
            info.origin = {};
            info.origin.iata = '';
            info.origin.muni = 'Origin'
        }

        if (info.destination === null) {
            info.destination = {};
            info.destination.iata = '';
            info.destination.muni = 'Destination'
        }

        if (info.airline == null) {
            info.airline = {};
            info.airline.name = "Unknown Airline"
        }

        selection = aircraft[info.aircraft.icao24];
        socket.emit('jetphotos.thumb', info.aircraft.reg);

        selection.marker.getElement().style.color = "lightgrey";

        document.getElementById('main-container-main-view').style.display = 'none';
        aircraftView = document.getElementById('main-container-aircraft-view')
        aircraftView.style.display = null;
        
        plotRoutes()

        aircraftView.innerHTML = `
            <img class="aircraft-img" id="img-${info.aircraft.reg}">
            <div class="aircraft-info">

                <div style="position: relative; top: 0; padding: 25px 0">
                    <span style="position: absolute; left: 0" id="back">&larr; ${info.airline.name}</span>
                    <span style="position: absolute; right: 0">${info.callsign}</span>
                </div>
                <hr>
                <div style="position: relative; opacity: 0.5; padding: 10px 0">
                    <span id="origin-${info.callsign}" style="position: absolute; left: 0">${info.origin.muni}</span>

                    <span id="destination-${info.callsign}" style="position: absolute; right: 0">${info.destination.muni}</span>
                </div>

                <div style="position: relative; margin: 0; padding-bottom: 50px">
                    <input id="origin-input" class="iata-input" style="position: absolute; left: 0" placeholder="${info.origin.iata}" contenteditable="true" required maxlength="3" minlength="3">

                    <input id="destination-input" class="iata-input" style="text-align: right; position: absolute; right: 0" placeholder="${info.destination.iata}" contenteditable="true" required maxlength="3" minlength="3">

                    <h1 style="position: absolute; left: 50%; transform: translateX(-50%)">&#x2708;</h1>
                </div>
                <progress style="width: 100%; position: relative" value="${polylines.percentage}" max="1"></progress>
            </div>`;

        let latlng = selection.marker.getLatLng();
        let point = map.latLngToContainerPoint(latlng);
        let xOffset = yOffset = 0;

        container.style.transition = 'height 0.3s ease';
        if (window.innerWidth > 500) {
            container.style.height = (window.innerHeight - 10) + "px";
            xOffset = -160
        } else {
            container.style.height = "350px";
            yOffset = 175
        }
        point.x += xOffset;
        point.y += yOffset;
        map.panTo(map.containerPointToLatLng(point));

        document.getElementById("origin-input").addEventListener("input", function() {
            if (this.value.length >= parseInt(this.getAttribute("maxlength"))) {
                let iata = this.value;
                socket.emit("lookup.airport", iata, `origin-${info.callsign}`);
            } else {
                document.getElementById(`origin-${info.callsign}`).innerHTML = 'Origin';
            }
        });

        document.getElementById("destination-input").addEventListener("input", function() {
            if (this.value.length >= parseInt(this.getAttribute("maxlength"))) {
                let iata = this.value;
                socket.emit("lookup.airport", iata, `destination-${info.callsign}`);
            } else {
                document.getElementById(`destination-${info.callsign}`).innerHTML = 'Destination';
            }
        });

        setMaxContainerHeight()
        document.getElementById('back').addEventListener('click', clearMap);
    });

    socket.on('jetphotos.thumb', function(image) {
        imageId = 'img-' + image.tail
        try {document.getElementById(imageId).src = image.url} catch {}
    });

    socket.on('lookup.airport', function(airport) {
        if (airport.routing !== null) {
            if (typeof airport.muni !== 'undefined') {
                document.getElementById(airport.routing).innerHTML = airport.muni
            }

            if (airport.routing.startsWith('origin-')) {
                if (selection.icao24 === polylines.icao24) {
                    info.origin = airport
                }
                socket.emit("lookup.add_origin", selection.callsign, airport.icao)
            } else if (airport.routing.startsWith('destination-')) {
                if (selection.icao24 === polylines.icao24) {
                    info.destination = airport
                }
                socket.emit("lookup.add_destination", selection.callsign, airport.icao)
            }
        }
    });
});
