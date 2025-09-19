# security.py
import shlex

class SecurityManager:
    """Handles validation of commands against a whitelist."""
    def __init__(self):
        # This defines the allowed EXECUTABLES. e.g., 'ls', 'df', 'uptime'
        self._allowed_executables = {
            "ls", "df", "uptime", "uname", "free"
        }
        print("✅ SecurityManager initialized.")

    def is_allowed(self, command: str) -> bool:
        """
        Checks if the base executable of a command is in the whitelist.
        Returns True if allowed, False otherwise.
        """
        if not command:
            return False
        
        try:
            # Safely get the first part of the command (the executable)
            base_command = shlex.split(command)[0]
            if base_command in self._allowed_executables:
                return True
            else:
                print(f"⚠️ SECURITY: Command '{base_command}' is not in the whitelist.")
                return False
        except (IndexError, ValueError):
            print(f"⚠️ SECURITY: Received an invalid or empty command string.")
            return False