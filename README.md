# MessageForwarder
A simple websocket server forwarding chat messages received from a livestream chat.

It is made to be used in combination with Twitch Heatmap Chat (https://github.com/FDMX2/Twitch-Heatmap-Chat)

## How it works:
Download the latest executable here ([https://github.com/FDMX2/MessageForwarder/releases](https://github.com/FDMX2/MessageForwarder/releases/latest)) and start it or run the main.py you find in the MsgForwarder folder (only if you have python 3.6 or higher installed).

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

## It uses:
  - Websocket Server (https://github.com/Pithikos/python-websocket-server) to simplify websocket handling
  - Chat downloader (https://github.com/xenova/chat-downloader) to receive the livestream messages

## License

The MIT License

Copyright (c) 2022 FDMX2 @ github
