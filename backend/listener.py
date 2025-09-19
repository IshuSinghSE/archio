import os
import sys
import warnings
import subprocess 
import shlex
from Adafruit_IO import MQTTClient

# Suppress the pkg_resources deprecation warning
warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API")

# Import configuration
try:
    from config import AIO_USERNAME, AIO_KEY, AIO_FEED_ID
except ImportError:
    print("❌ ERROR: config.py not found. Please create it with your Adafruit IO credentials.")
    sys.exit(1)

# --- Place this dictionary near the top of your script ---
ALLOWED_COMMANDS = {
    "list_files": "ls -lh",
    "check_space": "df -h",
    "uptime": "uptime",
    "system_info": "uname -a",
    "check_ram": "free -h"
}

# --- This is the new, much safer message function ---
def message(client, feed_id, payload):
    """Callback that executes a command ONLY if it's in the whitelist."""
    command_key = payload.strip()
    print(f"✅ Instruction Received: '{command_key}'")

    if command_key in ALLOWED_COMMANDS:
        command_to_run = ALLOWED_COMMANDS[command_key]
        print(f"🚀 Executing whitelisted command: '{command_to_run}'")
        try:
            # We still use shlex.split for good practice
            args = shlex.split(command_to_run)
            result = subprocess.run(args, capture_output=True, text=True, check=True, timeout=30)
            
            print("💻 Command Output:")
            print(result.stdout)
            # You can now confidently publish the output back!
            # client.publish('your-output-feed-id', result.stdout)

        except Exception as e:
            print(f"❌ An error occurred while executing '{command_to_run}': {e}")
    else:
        print(f"⚠️ SECURITY WARNING: Instruction '{command_key}' is not in the whitelist. Ignoring.")


def connected(client):
    """Callback function for when the client connects to Adafruit IO."""
    print("⚡️ Connected to Adafruit IO! Listening for commands on the '{0}' feed...".format(AIO_FEED_ID))
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

    client = MQTTClient(AIO_USERNAME, AIO_KEY)
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message

    try:
        client.connect()
    except Exception as e:
        print(f"❌ ERROR: Could not connect to Adafruit IO. Details: {e}")
        sys.exit(1)

    try:
        client.loop_blocking()
    except KeyboardInterrupt:
        client.disconnect()