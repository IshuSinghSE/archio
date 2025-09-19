# main.py
import sys
from agent import Agent
from listener import MQTTListener
import config
from Adafruit_IO import MQTTClient # Import the client here

def main():
    """Initializes and runs the agent and listener."""
    if config.AIO_USERNAME == "YOUR_ADAFRUIT_USERNAME":
        print("❌ ERROR: Please configure your Adafruit IO credentials in config.py")
        sys.exit(1)
    
    # 1. Create a single, shared MQTT client instance
    mqtt_client = MQTTClient(config.AIO_USERNAME, config.AIO_KEY)
    
    # 2. Create the agent, passing the client to it
    my_agent = Agent(mqtt_client=mqtt_client, command_file='commands.json')
    
    # 3. Create the listener, passing the SAME client and the agent's handler
    listener = MQTTListener(
        client=mqtt_client,
        feed_id=config.AIO_FEED_ID,
        message_callback=my_agent.handle_request
    )
    
    # 4. Start the listener
    listener.start_listening()

if __name__ == "__main__":
    main()