// Create a map and set its view to Konstanz with a certain zoom level
var map = L.map('map').setView([47.6636, 9.1758], 13);

// Add a tile layer to the map (OpenStreetMap tiles)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Add the specified points of interest with links
var pointsOfInterest = [
    { id: 1, name: "Max-Stromeyer-Straße 176", coords: [47.679610170451674, 9.150573142319644]},
    { id: 2, name: "Dettinger Straße", coords: [47.694316576346765, 9.142530658669918] },
    { id: 3, name: "Schwaketenstraße", coords: [47.68802596035806, 9.159333187466897] },
    { id: 4, name: "Konrad-Zuse-Straße", coords: [47.676906022627755, 9.161475478573882] },
    { id: 5, name: "An der Linde", coords: [47.674525329673415, 9.188143552111853] },
    { id: 6, name: "Luisenstraße", coords: [47.670806173358315, 9.185555294956334] },
    { id: 7, name: "Lorettosteig", coords: [47.67538410940641, 9.198787053233458] },
    { id: 8, name: "Mainaustraße 147", coords: [47.681695582897916, 9.202239181520447] },
    { id: 9, name: "Mainaustraße 234", coords: [47.69285229918978, 9.193330388228206] },
    { id: 10, name: "Gartenstraße", coords: [47.66646372589333, 9.163064668675899] },
    { id: 11, name: "Rheingutstaße", coords: [47.667281151838125, 9.166924063131988] }
];

// Loop through points and add them to the map with links
pointsOfInterest.forEach(function(point) {
    L.marker(point.coords).addTo(map)
        .bindPopup(`<b><h1>${point.name}</h1><a href="../zone/${point.id}" target="_blank">Öffnen</a></b>`)
});