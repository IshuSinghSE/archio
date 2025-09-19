import os
import sys
from Adafruit_IO import MQTTClient

# Import configuration
try:
    from config import AIO_USERNAME, AIO_KEY, AIO_FEED_ID
except ImportError:
    print("❌ ERROR: config.py not found. Please create it with your Adafruit IO credentials.")
    sys.exit(1)

# This function is called whenever a new message is received from the feed.
def message(client, feed_id, payload):
    """Callback function for receiving feed data."""
    print(f"✅ New Command Received: '{payload}'")
    # We will add the logic to execute the command here in the next step.
    # For now, we just print it.

def connected(client):
    """Callback function for when the client connects to Adafruit IO."""
    print("⚡️ Connected to Adafruit IO! Listening for commands on the '{0}' feed...".format(AIO_FEED_ID))
    # Subscribe to the feed specified in the configuration
    client.subscribe(AIO_FEED_ID)

def disconnected(client):
    """Callback function for when the client disconnects from Adafruit IO."""
    print("🔌 Disconnected from Adafruit IO!")
    sys.exit(1)

# Main script execution
if __name__ == "__main__":
    if AIO_USERNAME == "YOUR_ADAFRUIT_USERNAME" or AIO_KEY == "YOUR_ADAFRUIT_AIO_KEY":
        print("❌ ERROR: Please configure your Adafruit IO credentials in the script before running.")
        sys.exit(1)

    # Create an MQTT client instance.
    client = MQTTClient(AIO_USERNAME, AIO_KEY)

    # Assign the callback functions.
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message

    # Connect to Adafruit IO
    try:
        client.connect()
    except Exception as e:
        print(f"❌ ERROR: Could not connect to Adafruit IO. Check your credentials and internet connection. Details: {e}")
        sys.exit(1)

    # Start a blocking loop to listen for messages.
    # This will run forever until you press Ctrl+C in the terminal.
    client.loop_blocking()