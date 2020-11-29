// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/player_api";

var firstScriptTag = document.getElementsByTagName('script')[0];

firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
// after the API code downloads.
var player;

function onYouTubePlayerAPIReady() {
    var vids = [
        'lep7-tH15MY',
        'x1o2nr_euhM',
        '-4TgG0UZEnw',
        'lBAk0OabRDc',
        'tnGaCZZ5Z28',
        'atycPTJ6LWk',
        'lElrd62isec',
        'v7M_3_dGsWk',
        '3Thp_c47WEc',
        'JmLqoKYPgDc',
        'N7Ds28GQOM0',
    ]
    player = new YT.Player('ytplayer', {
        width: document.body.clientWidth,
        height: document.body.clientWidth,
        videoId: vids[Math.floor(Math.random() * vids.length)],
        playerVars: {
            'autoplay': 1,
            'showinfo': 0,
            'autohide': 1,
            'loop': 1,
            'controls': 0,
            'modestbranding': 1,
            'vq': 'hd1080',
            'disablekb': 1,
            're': 1,
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
    // event.target.setPlaybackRate(0.5);
    event.target.seekTo(15);
    event.target.playVideo();
    document.getElementById("ytplayer").style.marginTop = "-" + (document.body.clientWidth / 4) + "px";
    player.mute(); // comment out if you don't want the auto played video muted
}

// 5. The API calls this function when the player's state changes.
// The function indicates that when playing a video (state=1),
// the player should play for six seconds and then stop.
function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.ENDED) {
            player.seekTo(15);
            player.playVideo();
        }
    }
    function stopVideo() {
        player.stopVideo();
}


