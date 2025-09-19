# agent.py - A self-configuring Hybrid AI Assistant
import re
import os
import json
import datetime
import subprocess
import ollama
from config import OLLAMA_MODEL, AIO_FEEDBACK_ID # Import config to get the feedback feed name

class Agent:
    # The __init__ now accepts the mqtt_client
    def __init__(self, mqtt_client, command_file='commands.json'):
        self._mqtt_client = mqtt_client # Store the client
        self._rules = []
        self._function_map = {}
        self._ai_system_prompt = ""
        self._load_commands(command_file)
        print("🚀 Hybrid Agent is online and ready.")
        # ... (The rest of the __init__ and _load_commands methods are unchanged) ...
    
    # --- The _send_response method is now updated ---
    def _send_response(self, response: str):
        """Prints the response and publishes it back to the feedback feed."""
        print(f"📢 Response: {response}")
        try:
            print(f"📡 Publishing feedback to '{config.AIO_FEEDBACK_ID}'...")
            self._mqtt_client.publish(config.AIO_FEEDBACK_ID, response)
        except Exception as e:
            print(f"❌ Could not publish feedback to Adafruit IO. Error: {e}")
        print("-" * 30)

    # ... (All other methods in the Agent class remain exactly the same) ...

class Agent:
    def __init__(self, mqtt_client, command_file='commands.json'):
        self._mqtt_client = mqtt_client # Store the client
        self._rules = []
        self._function_map = {}
        self._ai_system_prompt = ""
        self._load_commands(command_file)
        print("🚀 Hybrid Agent is online and ready.")

        self._load_commands(command_file)

        print("🚀 Hybrid Agent is online and ready.")
        print(f"✅ Loaded {len(self._rules)} fast-lane rules and {len(self._function_map)} total skills.")
    
    # --- The _send_response method is now updated ---
    def _send_response(self, response: str):
        """Prints the response and publishes it back to the feedback feed."""
        print(f"📢 Response: {response}")
        try:
            print(f"📡 Publishing feedback to '{config.AIO_FEEDBACK_ID}'...")
            self._mqtt_client.publish(config.AIO_FEEDBACK_ID, response)
        except Exception as e:
            print(f"❌ Could not publish feedback to Adafruit IO. Error: {e}")
        print("-" * 30)

    def _load_commands(self, command_file):
        """Loads command definitions and dynamically builds agent capabilities."""
        # Map of intent names to the actual Python functions
        # This is the only place you need to link an intent to its code.
        available_functions = {
            "get_time": self.get_time,
            "list_running_apps": self.list_running_apps,
            "create_folder": self.create_folder,
            "open_website": self.open_website,
            "open_app": self.open_app,
            "search_web": self.search_web,
            "create_file": self.create_file,
            "change_wallpaper": self.change_wallpaper
        }
        
        with open(command_file, 'r') as f:
            commands = json.load(f)

        prompt_descriptions = []
        for cmd in commands:
            intent = cmd['intent']
            
            # Link the intent to its function if it exists
            if intent in available_functions:
                self._function_map[intent] = available_functions[intent]
                prompt_descriptions.append(f"- {intent}: {cmd['description']}")
                
                # If a regex pattern exists, create a fast-lane rule
                if 'pattern' in cmd:
                    self._rules.append({
                        "pattern": cmd['pattern'],
                        "function": available_functions[intent]
                    })
        
        # Dynamically build the AI's system prompt
        self._ai_system_prompt = (
            "You are an expert at converting user requests into structured JSON. "
            "Your response MUST be a single JSON object with 'intent' and 'entities' keys. "
            "Here are the available intents and their required entities:\n" +
            "\n".join(prompt_descriptions)
        )
        
    def handle_request(self, text: str):
        print("-" * 30)
        print(f"✅ New Request Received: '{text}'")
        
        for rule in self._rules:
            match = re.search(rule["pattern"], text, re.IGNORECASE)
            if match:
                print("⚡️ Fast lane match! Executing rule-based command.")
                response = rule["function"](*match.groups())
                self._send_response(response)
                return

        print("🧠 No fast lane match. Forwarding to AI model...")
        self._handle_with_ai(text)

    def _handle_with_ai(self, text: str):
        try:
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[
                    {'role': 'system', 'content': self._ai_system_prompt},
                    {'role': 'user', 'content': text},
                ],
                format='json'
            )
            analysis = json.loads(response['message']['content'])
            intent = analysis.get("intent")
            entities = analysis.get("entities", {})

            if intent in self._function_map:
                function_to_call = self._function_map[intent]
                api_response = function_to_call(**entities)
                self._send_response(api_response)
            else:
                self._send_response(f"Sorry, I understood the intent '{intent}', but I don't know how to do that.")
        except Exception as e:
            self._send_response(f"Sorry, I had trouble processing that with my AI brain. Error: {e}")

    def _send_response(self, response: str):
        print(f"📢 Response: {response}")
        # MQTT publish would go here
        print("-" * 30)
    
    # --- Skill Functions ---

    def get_time(self):
        return f"The time is {datetime.datetime.now().strftime('%I:%M %p')}."

    def list_running_apps(self):
        try:
            result = subprocess.run("ps -eo comm --sort=-pcpu | head -n 10", shell=True, capture_output=True, text=True, check=True)
            return f"Here are some top running processes:\n{result.stdout}"
        except: return "Sorry, I couldn't get the process list."

    def create_folder(self, folder_name: str = None):
        if not folder_name: return "You need to specify a folder name."
        path = os.path.expanduser(f"~/Desktop/{folder_name}")
        os.makedirs(path, exist_ok=True)
        return f"I've created the folder '{folder_name}' on your desktop."

    def create_file(self, file_name: str = None):
        if not file_name: return "You need to specify a file name."
        path = os.path.expanduser(f"~/Desktop/{file_name}")
        open(path, 'a').close()
        return f"I've created the file '{file_name}' on your desktop."

    def open_website(self, url: str = None):
        if not url: return "You need to specify a website URL."
        if not url.startswith(('http://', 'https://')): url = 'https://' + url
        subprocess.run(["xdg-open", url], check=True)
        return f"Opening {url} for you."

    def search_web(self, query: str = None):
        if not query: return "What would you like me to search for?"
        import urllib.parse
        search_url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
        return self.open_website(search_url)

    def open_app(self, app_name: str = None):
        if not app_name: return "You need to specify an application name."
        try:
            subprocess.Popen([app_name.lower()])
            return f"Starting {app_name}..."
        except FileNotFoundError:
            return f"Sorry, I can't find an app named '{app_name}'."
    
    def change_wallpaper(self, file_path: str = None):
        if not file_path or not os.path.isfile(file_path): return "You need to provide a valid path to an image file."
        uri_path = f"file://{os.path.abspath(file_path)}"
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri_path], check=True)
        return "As you wish. The wallpaper has been changed."