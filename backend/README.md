# JARVIS Backend Listener

This Python script listens for commands sent from the JARVIS Command Console web interface via Adafruit IO MQTT.

## Features

- Real-time MQTT connection to Adafruit IO
- **🔒 Secure command whitelist system** - Only predefined safe commands are executed
- Automatic command processing with output capture
- Error handling and connection recovery
- Timeout protection for long-running commands

## Security

### 🛡️ Command Whitelist System

The script uses a **secure whitelist approach** that only allows predefined, safe commands:

```python
ALLOWED_COMMANDS = {
    "list_files": "ls -lh",
    "check_space": "df -h",
    "uptime": "uptime",
    "system_info": "uname -a",
    "check_ram": "free -h"
}
```

**✅ Safe Commands:**
- `list_files` → `ls -lh` (List files with details)
- `check_space` → `df -h` (Check disk space)
- `uptime` → `uptime` (System uptime)
- `system_info` → `uname -a` (System information)
- `check_ram` → `free -h` (Memory usage)

**❌ Blocked Commands:**
- `rm -rf /` → ⚠️ SECURITY WARNING
- `sudo reboot` → ⚠️ SECURITY WARNING
- Any command not in the whitelist → ⚠️ SECURITY WARNING

### Test Security

Run the security test to see the whitelist in action:

```bash
python3 test_security.py
```

This will demonstrate:
- ✅ Whitelisted commands execute successfully
- ❌ Dangerous commands are blocked with warnings
- 📊 Command output is captured and displayed

## Setup

### Prerequisites

1. Install Python dependencies:
   ```bash
   pip install Adafruit_IO setuptools<81
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
python3 backend/listener.py
```

The script will:
1. Connect to Adafruit IO via MQTT
2. Subscribe to your command feed
3. Listen for incoming commands
4. **Only execute whitelisted commands**
5. Display command output and security warnings

## Adding New Commands

To add new safe commands to the whitelist:

1. Edit the `ALLOWED_COMMANDS` dictionary in `listener.py`
2. Add your command: `"command_key": "actual_command"`
3. Test with the security test script
4. Only add commands that are safe and necessary

## Security Best Practices

- ✅ **Whitelist-only execution** - Never execute arbitrary commands
- ✅ **Input validation** - All inputs are sanitized
- ✅ **Timeout protection** - Commands can't run indefinitely
- ✅ **Error handling** - Graceful failure handling
- ✅ **Output capture** - No command output leaks to console unexpectedly
- ✅ **Audit logging** - All command attempts are logged

## Next Steps

The current implementation executes system commands. You can extend it to:
- Control hardware (Raspberry Pi GPIO, Arduino)
- Send responses back to Adafruit IO feeds
- Integrate with other services (webhooks, APIs)
- Add user authentication and authorization
- Implement rate limiting for command execution