# listener.py
import sys
# The library is already imported in main.py, we only need the type hint
# from Adafruit_IO import MQTTClient 

class MQTTListener:
    """Manages the MQTT connection and message listening."""
    # The __init__ now accepts a pre-configured client object
    def __init__(self, client, feed_id: str, message_callback):
        self._client = client
        self._feed_id = feed_id
        self._message_callback = message_callback

        # Assign the callbacks to the client passed in
        self._client.on_connect = self._connected
        self._client.on_disconnect = self._disconnected
        self._client.on_message = self._message
        print("✅ MQTTListener initialized.")
        
    def _connected(self, client):
        print(f"⚡️ Connected to Adafruit IO! Listening on '{self._feed_id}' feed...")
        client.subscribe(self._feed_id)

    def _disconnected(self, client):
        print("🔌 Disconnected from Adafruit IO!")
        sys.exit(1)

    def _message(self, client, feed_id, payload):
        self._message_callback(payload)

    def start_listening(self):
        """Connects to the broker and starts the blocking loop."""
        print("Attempting to connect to Adafruit IO...")
        self._client.connect()
        try:
            self._client.loop_blocking()
        except KeyboardInterrupt:
            print("\n🔌 Disconnecting from Adafruit IO...")
            self._client.disconnect()