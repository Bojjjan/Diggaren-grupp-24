const baseURL = "http://127.0.0.1:5000/channels";

async function listChannels() {
  const options = {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  };

  const response = await fetch(baseURL, options);
  const channels = await response.json();
  const container = document.querySelector(".container .row"); 
  container.replaceChildren(); 

  channels.forEach((channel) => {
    const colDiv = document.createElement("div");
    colDiv.classList.add("col-6");

    const radioContentDiv = document.createElement("div");
    radioContentDiv.classList.add("d-flex", "align-items-center", "p-3", "radio-content");
    
    const channelImageDiv = document.createElement("div");
    channelImageDiv.classList.add("radio-icon", "me-3");
    const channelImage = document.createElement("img");

    let imageSrc = "defaultChannel.JPEG";
    if (channel.channel_img) {
      imageSrc = channel.channel_img;
    }
    channelImage.setAttribute("src", imageSrc);

    let imageAlt = "No channel image available";
    if (channel.channel_name) {
      imageAlt = channel.channel_name;
    }
    channelImage.setAttribute("alt", imageAlt);
    channelImage.setAttribute("width", "75");
    channelImage.setAttribute("height", "75");
    channelImageDiv.appendChild(channelImage);

    const albumCoverDiv = document.createElement("div");
    albumCoverDiv.classList.add("album-cover", "me-3");
    const albumImage = document.createElement("img");

    let albumSrc = "defaultChannel.JPEG";
    if (channel.album_image) {
      albumSrc = channel.album_image;
    }
    albumImage.setAttribute("src", albumSrc);

    let albumAlt = "No album image available";
    if (channel.song_title) {
      albumAlt = channel.song_title;
    }
    albumImage.setAttribute("alt", albumAlt);

    albumImage.setAttribute("width", "75");
    albumImage.setAttribute("height", "75");
    albumCoverDiv.appendChild(albumImage);

    const songInfoDiv = document.createElement("div");
    songInfoDiv.classList.add("song-info", "text-start");

    const songName = document.createElement("h5");
    songName.classList.add("mb-1");
    if (channel.song_title) {
      songName.textContent = channel.song_title;
    } else {
      songName.textContent = "No song playing";
    }

    const artistName = document.createElement("p");
    artistName.classList.add("mb-1");
    if (channel.artist_name) {
      artistName.textContent = channel.artist_name;
    } else {
      artistName.textContent = "Unknown artist";
    }

    const addSongBtn = document.createElement("button");
    addSongBtn.classList.add("add-song-btn");
    const addSongImg = document.createElement("img");
    addSongImg.src = "add_circle.svg";
    addSongImg.alt = "+";
    addSongImg.classList.add("add-song-img");
    

    songInfoDiv.appendChild(songName);
    songInfoDiv.appendChild(artistName);

    radioContentDiv.appendChild(channelImageDiv);
    radioContentDiv.appendChild(albumCoverDiv);
    radioContentDiv.appendChild(songInfoDiv);
    radioContentDiv.appendChild(addSongBtn);
    addSongBtn.appendChild(addSongImg);


    addSongBtn.addEventListener("click", (event) => {
      event.stopPropagation();
      showPlaylist(channel.spotify_id);
    });

    radioContentDiv.addEventListener("click", () => openModal(channel.id)); 

    colDiv.appendChild(radioContentDiv);
    container.appendChild(colDiv);
  });
}

function showPlaylist(songid){
  if(!loggedIn){
    openNotLoggedInModal()
    return
  }

  
  const label = document.getElementById("previousSongsModalLabel")
  label.innerHTML = "Select Playlist"

  const playlistsSection = document.getElementById("previous-songs-list");
  playlistsSection.innerHTML = ""; 

  

  playlists.forEach((playlist) => {
    let defaultImg = "defaultChannel.JPEG";

    const section = document.createElement("div");
    section.classList.add("playlistSection");

    const playlistImg = document.createElement("img");
    playlistImg.classList.add("playlistImg");
    
    if(playlist.image){
      defaultImg = playlist.image
    }

    playlistImg.src = playlist.image;

    const playlistName = document.createElement("p");
    playlistName.classList.add("playlistName");
    playlistName.innerHTML = playlist.name;

    //section.textContent = `${song.title} - ${song.artist}`;
    section.appendChild(playlistImg);
    section.appendChild(playlistName);
    playlistsSection.appendChild(section);

    section.addEventListener("click", () => {
        add_song_to_playlist(playlist.id, songid)
    })

  });

  const modal = new bootstrap.Modal(document.getElementById("previousSongsModal"));
  modal.show();
}

function openNotLoggedInModal() {  

  const label = document.getElementById("previousSongsModalLabel")
  label.innerHTML = "Not logged in."

  const songList = document.getElementById("previous-songs-list");
  songList.innerHTML = "Please log in and try again."; 

  const modal = new bootstrap.Modal(document.getElementById("previousSongsModal"));
  modal.show();
}           


function openModal(channelId) {  
  const previousSongs = [
    { title: "Låt-namn", artist: "Artist-namn" },
  ];

  const label = document.getElementById("previousSongsModalLabel")
  label.innerHTML = "Previous Songs"

  const songList = document.getElementById("previous-songs-list");
  songList.innerHTML = ""; 

  previousSongs.forEach((song) => {
    const listItem = document.createElement("li");
    listItem.textContent = `${song.title} - ${song.artist}`;
    songList.appendChild(listItem);
  });

  const modal = new bootstrap.Modal(document.getElementById("previousSongsModal"));
  modal.show();
}           

document.addEventListener("DOMContentLoaded", listChannels);


document.addEventListener("DOMContentLoaded", () => {
  listChannels();
  setInterval(listChannels, 60000); // 60 seconds
});