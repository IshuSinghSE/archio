# JARVIS Backend Listener

This Python script listens for commands sent from the JARVIS Command Console web interface via Adafruit IO MQTT.

## Features

- Real-time MQTT connection to Adafruit IO
- Automatic command processing
- Secure credential management
- Error handling and connection recovery

## Setup

### Prerequisites

1. Install Python dependencies:
   ```bash
   pip install Adafruit_IO
   ```

2. Configure your credentials:
   ```bash
   cd backend
   cp config.example.py config.py
   ```

3. Edit `config.py` with your Adafruit IO credentials:
   - `AIO_USERNAME`: Your Adafruit IO username
   - `AIO_KEY`: Your Adafruit IO key
   - `AIO_FEED_ID`: Your feed name (default: "jarvis-commands")

## Usage

Run the listener:
```bash
python backend/listener.py
```

The script will:
1. Connect to Adafruit IO via MQTT
2. Subscribe to your command feed
3. Listen for incoming commands
4. Print received commands to the console

## Security

- Never commit `config.py` to version control
- Use environment variables for production deployments
- Keep your Adafruit IO key secure

## Next Steps

The current implementation just prints received commands. You can extend the `message()` function to:
- Execute system commands
- Control hardware (Raspberry Pi, Arduino)
- Send responses back to Adafruit IO
- Integrate with other services