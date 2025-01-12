const client_id_url = "http://127.0.0.1:5000/client_id";
const playlist_url = "http://127.0.0.1:5000/user_playlists"
const redirectUri = "http://localhost:5000/callback"
const getCodeUrl = "http://127.0.0.1:5000/get_code"

const scopes = ["user-read-private", "user-read-email"];
const options = { method: "GET"};
const loginBtn = document.getElementById("spotify_login_btn")
const logoutBtn = document.getElementById("logout_btn")
let clientId = "";
let client_token = ""
let playlists = []
let loggedIn = false

async function get_code() {

    const response = await fetch(getCodeUrl, options);
    const data = await response.json();

    if (client_token === "") {
        client_token = data.code;
        get_playlists();
    }
}

async function get_client_id() {
    const response = await fetch(client_id_url, options);
    const data = await response.json();
    clientId = data.client_id
}

async function add_song_to_playlist(){

}


async function get_playlists() {
    const response = await fetch(playlist_url+"?access_token="+client_token, options);
    const data = await response.json();
    
    data.forEach(element => {
        const playlist = new Playlist(element.name, element.id, element.image)
        playlists.push(playlist)
        console.log("Playlist added: " + playlist.name)
    });
}

function activateLogin(){
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

function activateLogout(){
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

activateLogin()
activateLogout()

class Playlist{
    constructor(name, id, image){
        this.name = name
        this.id = id
        this.image = image
    }
}
