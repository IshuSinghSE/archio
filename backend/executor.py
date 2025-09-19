# executor.py
import subprocess
import shlex

class CommandExecutor:
    """Executes validated shell commands."""
    def __init__(self):
        print("✅ CommandExecutor initialized.")

    def execute(self, command: str) -> tuple[bool, str]:
        """
        Executes a command and returns a tuple of (success, output).
        """
        try:
            args = shlex.split(command)
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            return (True, result.stdout)
        except FileNotFoundError:
            output = f"❌ Command not found: '{shlex.split(command)[0]}'"
            return (False, output)
        except subprocess.CalledProcessError as e:
            output = f"❌ Error executing command:\n{e.stderr}"
            return (False, output)
        except subprocess.TimeoutExpired:
            output = f"⌛️ Command '{command}' timed out."
            return (False, output)
        except Exception as e:
            output = f"❌ An unexpected error occurred: {e}"
            return (False, output)