// Create a map and set its view to Konstanz with a certain zoom level
var map = L.map('map').setView([47.6636, 9.1758], 13);

// Add a tile layer to the map (OpenStreetMap tiles)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Add the specified points of interest with links
var pointsOfInterest = [
    { name: "Max-Stromeyer-Straße 176", coords: [47.679610170451674, 9.150573142319644], url: "https://www.google.com/maps?q=Max-Stromeyer-Stra%C3%9Fe+176" },
    { name: "Dettinger Straße", coords: [47.694316576346765, 9.142530658669918], url: "https://www.google.com/maps?q=Dettinger+Stra%C3%9Fe" },
    { name: "Schwaketenstraße", coords: [47.68802596035806, 9.159333187466897], url: "https://www.google.com/maps?q=Schwaketenstra%C3%9Fe" },
    { name: "Konrad-Zuse-Straße", coords: [47.676906022627755, 9.161475478573882], url: "https://www.google.com/maps?q=Konrad-Zuse-Stra%C3%9Fe" },
    { name: "An der Linde", coords: [47.674525329673415, 9.188143552111853], url: "https://www.google.com/maps?q=An+der+Linde" },
    { name: "Luisenstraße", coords: [47.670806173358315, 9.185555294956334], url: "http://127.0.0.1:5500/index.html" },
    { name: "Lorettosteig", coords: [47.67538410940641, 9.198787053233458], url: "https://www.google.com/maps?q=Lorettosteig" },
    { name: "Mainaustraße 147", coords: [47.681695582897916, 9.202239181520447], url: "https://www.google.com/maps?q=Mainaustra%C3%9Fe+147" },
    { name: "Mainaustraße 234", coords: [47.69285229918978, 9.193330388228206], url: "https://www.google.com/maps?q=Mainaustra%C3%9Fe+234" },
    { name: "Gartenstraße", coords: [47.66646372589333, 9.163064668675899], url: "https://www.google.com/maps?q=Gartenstra%C3%9Fe" },
    { name: "Rheingutstaße", coords: [47.667281151838125, 9.166924063131988], url: "https://www.google.com/maps?q=Rheingutsta%C3%9Fe" }
];

// Loop through points and add them to the map with links
pointsOfInterest.forEach(function(point) {
    L.marker(point.coords).addTo(map)
        .bindPopup(`<b><a href="${point.url}" target="_blank">${point.name}</a></b>`)
        .openPopup();
});