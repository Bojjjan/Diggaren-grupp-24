const client_id_url = "http://127.0.0.1:5000/client_id";
const redirectUri = "http://localhost:5000/callback"
const getCodeUrl = "http://127.0.0.1:5000/get_code"


const scopes = ["user-read-private", "user-read-email"];
const options = { method: "GET"};

let clientId = "";
let client_token = ""

async function get_code() {
    const response = await fetch(getCodeUrl, options);
    const data = await response.json();
    client_token = data.code
}


async function get_client_id() {
    const response = await fetch(client_id_url, options);
    const data = await response.json();
    clientId = data.client_id
}

document.getElementById("spotify_login_btn").addEventListener("click", () => {
    
    const authUrl = `https://accounts.spotify.com/authorize?client_id=${clientId}&response_type=code&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scopes)}`;

    window.open(authUrl, "Spotify Login", "width=500,height=600");
    get_code()

});

get_client_id()