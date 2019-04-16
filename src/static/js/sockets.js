$(document).ready(function() {
    let socket = io.connect('https://' + document.domain + ':' + location.port);
    socket.on('connect', function () {
        socket.emit({data: "I'm connected!"});
    });
});