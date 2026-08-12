import subprocess

# 1. Define the actual tool function
def execute_shell_command(command: str) -> str:
    """Executes a terminal command and returns stdout or stderr."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

# 2. Map tool names to Python functions
TOOL_MAP = {
    'execute_shell_command': execute_shell_command
}

# 3. Provide schema representations for Ollama
TOOLS_SCHEMA = [
    {
        'type': 'function',
        'function': {
            'name': 'execute_shell_command',
            'description': 'Execute safe terminal shell commands on the local machine.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'command': {
                        'type': 'string',
                        'description': 'The exact bash or shell command to run.',
                    }
                },
                'required': ['command'],
            },
        },
    }
] 

