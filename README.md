<div align="center">
  <h1><strong>🎧 Diggaren 🎷</strong></h1>
</div>

## About
**Diggaren** is a tool that enhances your radio listening experience by connecting Sveriges Radio and Spotify. Here's what it does:  
- Displays the currently playing song on Sveriges Radio.  
- Fetches the album art and song details using Spotify.  
- Allows you to easily add the song to a Spotify playlist.  
- Shows the full list of songs played by a specific radio channel throughout the day.

This project was developed as part of a school assignment to explore APIs and build practical tools.

<br>

## Getting Started

Follow these steps to get started with Diggaren:

### 1. Install Python
Ensure that Python 3.12 or higher is installed. <br>You can download it from the official Python website:
[Download Python](https://www.python.org/downloads/)
> [!IMPORTANT]
> Python needs to be installed in  your system's PATH environment variable in order for this script to work. <br>
> If you don't know what system's PATH environment variable is, then this message can be ignored.

<br>

### 2. Clone the Repository
Clone the Diggaren repository using the following command in the terminal:

```bash
git clone https://github.com/Bojjjan/Diggaren-grupp-24.git
```

<br>

### 3. Open the Start Script
Open ```Diggaren-grupp-24``` folder and the run the appropriate script based on your operating system: <br>
Windows: ```start.bat``` <br>
Mac/Linux: ```start.sh```


> [!NOTE]
> In order for the script to work on Mac/Linux, you must first make the script runnable by using the following command:
> ```bash
> chmod +x start.sh
> ./start.sh
> ```





<br>
<br>


### Alternative: Setting Up a Virtual Environment
To manually set up the environment:
1. Navigate to the project folder:
```bash
 cd /path/to/project
```
2. Run the setup script:
```bash
 python setup_env.py
```
3. Install dependencies:
```bash
 pip install -e .
```
All required packages and dependencies are now installed.