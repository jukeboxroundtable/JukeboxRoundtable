$(document).ready(function () {
    let socket = io.connect('https://' + document.domain + ':' + location.port);

    socket.on('connect', function () {
        console.log("Connected")
    });

    $('#new_song').on('submit', function (e) {
        e.preventDefault();
        socket.emit('song_search', {search: $('#song_search_text').val()});
    });

    socket.on('search_results', function (data) {
        document.getElementById("title0").innerHTML = data[0].title;
        document.getElementById("title1").innerHTML = data[1].title;
        document.getElementById("title2").innerHTML = data[2].title;
        document.getElementById("title3").innerHTML = data[3].title;
        document.getElementById("title4").innerHTML = data[4].title;

        document.getElementById("url0").innerHTML = data[0].url;
        document.getElementById("url1").innerHTML = data[1].url;
        document.getElementById("url2").innerHTML = data[2].url;
        document.getElementById("url3").innerHTML = data[3].url;
        document.getElementById("url4").innerHTML = data[4].url;

        document.getElementById("thumbnail0").innerHTML = data[0].thumbnail;
        document.getElementById("thumbnail1").innerHTML = data[1].thumbnail;
        document.getElementById("thumbnail2").innerHTML = data[2].thumbnail;
        document.getElementById("thumbnail3").innerHTML = data[3].thumbnail;
        document.getElementById("thumbnail4").innerHTML = data[4].thumbnail;

        console.log(data);
    });

    socket.on('party_destroyed', function (data) {
        console.log("Party destroyed!");
        $.get("/_remove_session");
    });
});