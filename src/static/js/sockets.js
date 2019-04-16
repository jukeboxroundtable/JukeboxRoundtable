$(document).ready(function() {
    let socket = io.connect('https://' + document.domain + ':' + location.port);

    socket.on('connect', function () {
        console.log("Connected")
    });

    socket.on('news', function (data) {
       console.log(data);
    });
});