let map;

function initMap() {
    map = L.map('map').setView([0, 0], 2); // Initial position and zoom level

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    // Fetch existing truck data
    fetch('/get_data')
        .then(response => response.json())
        .then(data => {
            for (let id in data) {
                const source = data[id].source_address;
                const destination = data[id].destination_address;
                getCoordinates(source).then(sourceCoords => {
                    if (sourceCoords) {
                        const lorryIcon = L.icon({
                            iconUrl: 'https://icons.iconarchive.com/icons/bartkowalski/1960-matchbox-cars/128/Cattle-Truck-icon.png', // Path to the truck icon
                            iconSize: [32, 32], // Size of the icon
                            iconAnchor: [16, 32], // Point of the icon which will correspond to marker's location
                            popupAnchor: [0, -32] // Point from which the popup should open relative to the iconAnchor
                        });

                        L.marker([sourceCoords.lat, sourceCoords.lng], { icon: lorryIcon }).addTo(map)
                            .bindPopup(`Source: ${source}`).openPopup();
                    }
                });

                // Get coordinates and add markers for source and destination
                getCoordinates(source).then(sourceCoords => {
                    if (sourceCoords) {
                        L.marker([sourceCoords.lat, sourceCoords.lng]).addTo(map)
                            .bindPopup(`Source: ${source}`).openPopup();
                    }
                });

                getCoordinates(destination).then(destCoords => {
                    if (destCoords) {
                        L.marker([destCoords.lat, destCoords.lng]).addTo(map)
                            .bindPopup(`Destination: ${destination}`).openPopup();
                    }
                });
                getCoordinates(destination).then(destCoords => {
                    if (destCoords) {
                        drawRoute(sourceCoords, destCoords);
                    }
                });
            }
        });
}

function getCoordinates(address) {
    return fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(address)}&format=json&limit=1`)
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                return { lat: parseFloat(data[0].lat), lng: parseFloat(data[0].lon) };
            }
            return null;
        });
}

// Initialize the map on page load
window.onload = initMap;