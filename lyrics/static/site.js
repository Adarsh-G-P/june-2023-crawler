function update_lyrics(data) {
    $("h3.track").html(data.name);
    $("#track-lyrics").html(data.lyrics);
    $("#lyrics-container").append("<p>" + data.lyrics + "</p>");
}



function click_handler(ev) {
    
    ev.preventDefault();
    $("p.songs").html("Loading ....");
    $.ajax({url : ev.target.href,
        dataType:'json',
            headers : {"Accept": "application/json"},
            success: update_lyrics
    });
   
    }


function main() {
    $("ol.artists a").click(click_handler);
    }

$(main);