# TextBox

Copy text between machines on the same network. No signup, no install, no dependencies beyond Python3 and http.server.

## How it works

One machine runs the server. Any device on the same network opens the server's IP in a browser, pastes text, and hits Save. Another device opens the same address and the text is already there — hit Copy to grab it.

Text is stored in memory only. It resets when the server stops.

## Usage

```
python3 textbox.py
```

Then open `http://<your-local-ip>` from any device on the network.

> Port 80 requires `sudo`. Edit `port` in `textbox.py` to use a different one.

## Requirements

- Python 3
- http.server
