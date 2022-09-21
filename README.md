# MessageForwarder
A simple websocket server forwarding chat messages received from a livestream chat.

It is made to be used in combination with Twitch Heatmap Chat (https://github.com/FDMX2/Twitch-Heatmap-Chat)


## How to use:
Download the latest executable here (https://github.com/FDMX2/MessageForwarder/releases) and start it or run the main.py you find in the MsgForwarder folder (only if you have python 3.6 or higher installed).

The server is now ready to serve messages from livestreams. You can connect via the default port 13254.

### Example usage with Twitch Heatmap Chat
1. Open the Twitch Heatmap Chat (https://fdmx2.github.io/Twitch-Heatmap-Chat/) in your browser.
2. As Channel name enter the webscoket address and livestream url separated by | like so:
```
ws://ws_address|LIVESTREAM_URL
```
For example if you run the server on the same machine:
```
ws://127.0.0.1:13254|https://www.youtube.com/watch?v=VIDEOID
```

## Supported services
MessageForwarder only forwards the messages from the chat downloader (https://github.com/xenova/chat-downloader) thus supporting all services it does. In the current version (0.2.0) these services are:
-  YouTube.com - Livestreams, past broadcasts and premieres.
-  Twitch.tv - Livestreams, past broadcasts and clips.
-  Reddit.com - Livestreams, past broadcasts


## How to compile
For creating the stand alone executable out of the main.py yourself you can do the following:
1. Ensure you have python 3.6 or higher installed or download it from python.org
2. Open a command prompt, Powershell or bash
3. In your command prompt move to the folder you want to use
4. Create a virtual environment by typing in:
    ```
    python -m venv MsgForwarder
    ```
    This will create a the MsgForwarder folder
5. Activate the created virtual environment by typing in:
    ```
    MsgForwarder\Scripts\activate
    ```
    (for command prompt use *activate.bat* and for Powershell *actiavte.ps1* instead of *activate*)
6. Copy the *main.py* and *requirements.txt* from the repository into your created MsgForwarder folder
7. Move your command prompt to the created MsgForwarder folder
8. Install the necessary dependencies via your command prompt:
    ```
    python -m pip install -r requirements.txt
    ```
9. For testing you can run the main.py via
    ```
    python main.py
    ```
10. If everything works close the program by pressing *CTRL* + *c* in your command prompt
11. Finally compile it by typing:
    ```
    pyinstaller --onefile -F --collect-data chat_downloader main.py
    ```
12. After execution you should now have the main executable in the *dist* folder
## It uses:
  - Websocket Server (https://github.com/Pithikos/python-websocket-server) to simplify websocket handling
  - Chat downloader (https://github.com/xenova/chat-downloader) to receive the messages


## License

The MIT License

Copyright (c) 2022 FDMX2 @ github
