# JARVIS Command Console

A web-based interface for sending commands to JARVIS via Adafruit IO.

## Features

- Dark theme interface
- Voice input support (use voice keyboard)
- Real-time command sending to Adafruit IO
- Status feedback

## Setup

1. Clone this repository
2. Copy `config.example.js` to `config.js`
3. Edit `config.js` and add your Adafruit IO credentials:
   - `AIO_USERNAME`: Your Adafruit IO username
   - `AIO_KEY`: Your Adafruit IO key
   - `FEED_NAME`: Your feed name (default: "jarvis-commands")
4. Open `index.html` in a web browser

## Configuration

Create a `config.js` file with your Adafruit IO credentials:

```javascript
const CONFIG = {
    AIO_USERNAME: "your_username",
    AIO_KEY: "your_adafruit_io_key", 
    FEED_NAME: "jarvis-commands"
};
```

**Note:** Never commit your `config.js` file to version control as it contains sensitive API keys.

## Usage

1. Open `index.html` in your web browser
2. Type or use voice input to enter commands
3. Click "Execute" or press Enter to send the command
4. Check the status message for feedback

## Security

This project uses a local configuration file (`config.js`) to store sensitive credentials. This file is ignored by Git to prevent accidentally committing API keys to the repository.