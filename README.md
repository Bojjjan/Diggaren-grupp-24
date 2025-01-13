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
Navigate to the ```Diggaren-grupp-24``` folder and run the appropriate script based on your operating system: <br>
* Windows: ```start.bat``` <br>
* Mac/Linux: ```start.sh```


> [!NOTE]
> In order for the script to work on Mac/Linux, you must first make the script runnable by using the following command:
> ```bash
> chmod +x start.sh
> ./start.sh
> ```





<br>
<br>


## Manual installation
Follow steps "1. Install Python" and "2. Clone the Repository" as outlined above. <br>
Then open the  ```Diggaren-grupp-24``` folder and open a terminal in that folder. <br>

> [!NOTE]
> On Windows, open Command Prompt.


### 3. Creating a virtual environment

#### Step 1: Create and activate virtual environment
Run the following to create and activate the virtual environment: <br>
Windows (Command Prompt)
```bash
 python -m venv venv
 venv\Scripts\Activate

```

> [!IMPORTANT]
> On some Windows machines the script above does not work. Then run this script:
>```bash
>Set-ExecutionPolicy Unrestricted -Scope Process
>python -m venv .venv
>.venv/scripts/activate
>
>```

<br>

macOS/ Linux:
```bash
 python -m venv venv
 source venv/bin/activate

```
> [!NOTE]
> If everything is done correctly, ```(venv)``` should appear in the command line prompt.


#### Step 2: Installing dependencies
Once the virtual environment is active, install the required dependencies:
```bash
 pip install -r requirements.txt
```
<br>

### 4. start the server
With the virtual environment still active, start the server by running:
```bash
 python src\main\server\server.py
```
### 5. start the website
Once the server is running, open a new terminal window, navigate to the ```Diggaren-grupp-24```  folder, and run the following to open the frontend in your browser::
```bash
 src\frontend\index.html
```

A web browser should open, and the application will be running.
