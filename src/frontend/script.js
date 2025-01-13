const baseURL = "http://127.0.0.1:5000/channels";

/**
* Fetches a list of radio channels via a GET method and displays them in the interface with dynamically created HTML elements.
* Displays radio channel image, album cover, song title, and artist name.
*/
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
    radioContentDiv.classList.add(
      "d-flex",
      "align-items-center",
      "p-3",
      "radio-content"
    );

    const channelImageDiv = document.createElement("div");
    channelImageDiv.classList.add("radio-icon", "me-3");
    const channelImage = document.createElement("img");

    let imageSrc = "defaultChannel.JPEG";
    if (channel.channel_img) {
      imageSrc = channel.channel_img;
    }
    channelImage.setAttribute("src", imageSrc);

    let imageAlt = "No image available";
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

    let albumAlt = "No image available";
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

    radioContentDiv.addEventListener("click", () =>
      openModal(channel.channel_id, channel.channel_name)
    );
    colDiv.appendChild(radioContentDiv);
    container.appendChild(colDiv);
  });
}
/**
 * Shows all avalible playlist in your spotify account in a popup.
 */
function showPlaylist(songid) {
  if (!loggedIn) {
    statusMessageModal("Not logged in.", "Please log in and try again.");
    return;
  } else if (Object.keys(playlists).length === 0) {
    statusMessageModal(
      "No playlist found",
      "There are no playlists available."
    );
    return;
  }

  const label = document.getElementById("previousSongsModalLabel");
  label.innerHTML = "Select Playlist";

  const playlistsSection = document.getElementById("previous-songs-list");
  playlistsSection.innerHTML = "";

  playlists.forEach((playlist) => {
    let defaultImg = "defaultChannel.JPEG";

    const section = document.createElement("div");
    section.classList.add("playlistSection");

    const playlistImg = document.createElement("img");
    playlistImg.classList.add("playlistImg");

    if (playlist.image) {
      defaultImg = playlist.image;
    }

    playlistImg.src = playlist.image;

    const playlistName = document.createElement("p");
    playlistName.classList.add("playlistName");
    playlistName.innerHTML = playlist.name;

    section.appendChild(playlistImg);
    section.appendChild(playlistName);
    playlistsSection.appendChild(section);

    section.addEventListener("click", () => {
      add_song_to_playlist(playlist.id, songid, playlist.name);
    });
  });

  const modal = new bootstrap.Modal(
    document.getElementById("previousSongsModal")
  );
  modal.show();
}

/**
 * shows a popup for status message
 */
function statusMessageModal(title, text) {
  const label = document.getElementById("previousSongsModalLabel");
  label.innerHTML = title;

  const songList = document.getElementById("previous-songs-list");
  songList.innerHTML = text;

  const modal = new bootstrap.Modal(
    document.getElementById("previousSongsModal")
  );
  modal.show();
}

/**
*  Opens a popup window that shows previously played songs on the selected radio channel.
*/
async function openModal(channelId, channelName) {
  const modalTitle = document.getElementById("previousSongsModalLabel");
  const songList = document.getElementById("previous-songs-list");
  const modalElement = document.getElementById("previousSongsModal");
  modalTitle.textContent = channelName + " - Previous Songs";

  const apiUrl = baseURL + "/" + channelId;
  const response = await fetch(apiUrl, { method: "GET" });

  if (response.ok) {
    const history = await response.json();
    songList.replaceChildren();
    history.forEach(function (song) {

      const listItem = document.createElement("li");
      let title = "Unknown Title";
      if (song.song_title) {
        title = song.song_title;
      }

      let artist = "Unknown Artist";
      if (song.artist_name) {
        artist = song.artist_name;
      }
      listItem.innerHTML ="<strong>Song: </strong>" + title + " <strong>| Artist: </strong>" + artist;
      songList.appendChild(listItem);
    });
  } else {
    songList.innerHTML = "<li>Could not load channel history.</li>";
  }

  const modal = new bootstrap.Modal(modalElement);
  modal.show();
}

document.addEventListener("DOMContentLoaded", listChannels);


document.addEventListener("DOMContentLoaded", () => {
  listChannels();
  setInterval(listChannels, 60000); // 60 seconds
});
