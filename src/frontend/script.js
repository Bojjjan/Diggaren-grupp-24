    const baseURL = "http://127.0.0.1:5001/channels";
    
    async function listChannels() {
      const options = {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      };
      const response = await fetch(baseURL, options);
      const channels = await response.json();
      const channelList = document.querySelector("#channels");
      channelList.replaceChildren(); 
    
      channels.forEach((channel) => {
        let listItem = document.createElement("li");
        listItem.setAttribute("data-id", channel.channel_id);
        listItem.textContent = channel.channel_name; 
        listItem.addEventListener("click", fetchThenDisplayChannel);
        channelList.appendChild(listItem);
      });
    }
    
    async function fetchThenDisplayChannel(event) {
      const channelId = event.target.getAttribute("data-id");
      const url = `${baseURL}/${channelId}`;
      const options = {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      };
      const response = await fetch(url, options);
      const channel = await response.json();          
      displayChannel(channel);
    }
    
    function displayChannel(channel) {
      const image = document.createElement("img");
      image.setAttribute("src", channel.album_image);
      image.setAttribute("alt", channel.song_title);
    
      document.querySelector("#channelName").innerHTML = channel.channel_name;
      document.querySelector("#albumImageContainer").replaceChildren(image);
      document.querySelector("#songTitle").innerHTML = channel.song_title;
      document.querySelector("#artistName").innerHTML = channel.artist_name;
    
      document.querySelector("#existingChannel input[name=id]").value = channel.channel_id;
      document.querySelector("#existingChannel input[name=name]").value = channel.channel_name;
      document.querySelector("#existingChannel input[name=album_image]").value = channel.album_image;
      document.querySelector("#existingChannel input[name=song_title]").value = channel.song_title;
      document.querySelector("#existingChannel input[name=artist_name]").value = channel.artist_name;
    }
    
    document.addEventListener("DOMContentLoaded", listChannels);