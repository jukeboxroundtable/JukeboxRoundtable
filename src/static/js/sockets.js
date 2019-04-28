$(document).ready(function () {
    let socket = io.connect('https://' + document.domain + ':' + location.port);

    socket.on('connect', function () {
        console.log("Connected")
    });

    $('#new_song').on('submit', function (e) {
        e.preventDefault();
        socket.emit('song_search', {search: $('#song_search_text').val()});
    });
});