// Debug.js
// Remove from final

function bearing(point1, point2) {
    const degreesToRadians = degrees => degrees * Math.PI / 180;
    const radiansToDegrees = radians => radians * 180 / Math.PI;
    
    const lat1Rad = degreesToRadians(point1[0]);
    const lon1Rad = degreesToRadians(point1[1]);
    const lat2Rad = degreesToRadians(point2[0]);
    const lon2Rad = degreesToRadians(point2[1]);
    
    const deltaLon = lon2Rad - lon1Rad;
    
    const y = Math.sin(deltaLon) * Math.cos(lat2Rad);
    const x = Math.cos(lat1Rad) * Math.sin(lat2Rad) -
    Math.sin(lat1Rad) * Math.cos(lat2Rad) * Math.cos(deltaLon);
    let theta = Math.atan2(y, x);
    
    if (theta < 0) {
        theta += 2 * Math.PI;
    }
    
    const directionDegrees = (radiansToDegrees(theta) + 360) % 360;
    
    return directionDegrees;
}

function fly(aircraft, heading, speed) {
    setHeading(aircraft, heading)
	let speedMps = speed * 0.514444;
	let distance = speedMps * 0.01;
	let headingRad = heading * Math.PI / 180;
	setInterval(function() {
    	var latLng = aircraft.getLatLng();
    	var newLat = latLng.lat + (Math.cos(headingRad) * (distance / 111111));
    	var newLng = latLng.lng + (Math.sin(headingRad) * (distance / (111111 * Math.cos(latLng.lat * Math.PI / 180))));
    	aircraft.setLatLng([newLat, newLng]);
    }, 10);
}

// Add demo aircraft
aircraft.push(L.marker([51.5, -0.09], {
id: '40779a',
icon: planeIcon
}).addTo(map));

aircraft.push(L.marker([51.6, -0.1], {
id: 'copter',
icon: helicopterIcon
}).addTo(map));

setHeading(aircraft[0],270)
