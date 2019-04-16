$(document).ready(function() {
    let socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function () {
        socket.emit({data: "I'm connected!"});
    });
});