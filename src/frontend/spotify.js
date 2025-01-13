const client_id_url = "http://127.0.0.1:5000/client_id";
const playlist_url = "http://127.0.0.1:5000/user_playlists"
const redirectUri = "http://localhost:5000/callback"
const getCodeUrl = "http://127.0.0.1:5000/get_code"
const addSongToPlaylistUrl = "http://127.0.0.1:5000/add_song_to_playlist"

const scopes = ["user-read-private", "user-read-email", "playlist-modify-public", "playlist-modify-private", "playlist-read-private", "playlist-read-collaborative"];
const options = { method: "GET"};
const optionsPost = { method: "POST"};
const loginBtn = document.getElementById("spotify_login_btn")
const logoutBtn = document.getElementById("logout_btn")
let clientId = "";
let client_token = ""


let playlists = []
let loggedIn = false


/**
 * This function fetches the Spotify user token from the server.
 */
async function get_code() {

    const response = await fetch(getCodeUrl, options);
    const data = await response.json();

    if (client_token === "") {
        client_token = data.code;
        get_playlists();
    }
}


/**
 * This function fetches the client_id from the server.
 */
async function get_client_id() {
    const response = await fetch(client_id_url, options);
    const data = await response.json();
    clientId = data.client_id
}

/**
 * Sends a request to the server to add the specified song to the users specified playlist.
 */

async function add_song_to_playlist(playlistID, songID, nameOfPlaylist) {
    songID = "spotify:track:"+songID
    const response = await fetch(`${addSongToPlaylistUrl}?access_token=${encodeURIComponent(client_token)}&track_uris=${encodeURIComponent(songID)}&playlist_id=${encodeURIComponent(playlistID)}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        }
    });

    
    if (!response.ok) {
        console.error(`Error: ${response.status} ${response.statusText}`);
        return;
    }else {

        const section = document.createElement("div");
        section.classList.add("notification");

        const notificationMessage = document.createElement("p")
        notificationMessage.classList.add("message");
        notificationMessage.innerHTML = "Song added to " + nameOfPlaylist;

        const checkMark = document.createElement("img");
        checkMark.classList.add("checkMark");
        checkMark.src = "check_circle.svg"

        section.appendChild(checkMark);
        section.appendChild(notificationMessage);
        document.body.appendChild(section);

        
        setTimeout(() => {
            section.classList.add("fade-out");
        }, 2000);

        
        setTimeout(() => {
            section.remove();
        }, 3000);
        
    }

}

/**
 * This function fetches the users playlist from the server and adds them to the "playlists" list.
 */
async function get_playlists() {
    const response = await fetch(playlist_url+"?access_token="+client_token, options);
    const data = await response.json();
    
    data.forEach(element => {
        const playlist = new Playlist(element.name, element.id, element.playlist_image)
        playlists.push(playlist)
    });
}

/**
 * Sets up the login button to function properly.
 */

function setupLogin(){
    loginBtn.addEventListener("click", async () => {
        if(!loggedIn){
            await get_client_id()
            const authUrl = `https://accounts.spotify.com/authorize?client_id=${clientId}&response_type=code&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scopes)}`;

            window.open(authUrl, "Spotify Login", "width=500,height=600");
            loggedIn = true
            loginBtn.style.visibility = "hidden"
            logoutBtn.style.visibility = "visible"
            await get_code();
        }
    });
}


/**
 * Sets up the logout button to function properly.
 */
function setupLogout(){
    logoutBtn.style.visibility = "hidden";
    logoutBtn.addEventListener("click", async () => {
        if(loggedIn){
            loggedIn = false
            clientId = "";
            client_token = ""
            playlists = []
            loginBtn.style.visibility = "visible"
            logoutBtn.style.visibility = "hidden"
        }
    })
}

setupLogin()
setupLogout()


/**
 * This class is used to save data about a playlist.
 */
class Playlist{
    constructor(name, id, image){
        this.name = name
        this.id = id
        this.image = image
    }
}