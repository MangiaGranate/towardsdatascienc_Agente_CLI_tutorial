import subprocess
from ddgs import DDGS

# 1. Define the actual tool function
def execute_shell_command(command: str) -> str:
    """Executes a terminal command and returns stdout or stderr."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)


def secret_word():
    """Funzione di prova"""
    return "PATATA"


def ricerca_web(domanda: str, max_risultati: int = 5) -> str:
    """
    Cerca su internet usando DuckDuckGo
    
    Args:
        domanda: la query di ricerca
        max_risultati: numero massimo di risultati da restituire
    
    Returns:
        Una stringa formattata con i risultati della ricerca
    """
    try:
        print(f"Cerco su internet: '{domanda}'")
        
        # Usa la libreria duckduckgo-search (gratuita)
        with DDGS() as ddgs:
            risultati = list(ddgs.text(domanda, max_results=max_risultati))
        
        if not risultati:
            return "Nessun risultato trovato per questa ricerca."
        
        # Formatta i risultati in modo leggibile
        output = f"Risultati della ricerca per '{domanda}':\n\n"
        for i, r in enumerate(risultati, 1):
            output += f"{i}. {r.get('title', 'Senza titolo')}\n"
            output += f"   {r.get('body', '')[:200]}...\n"
            output += f"   Fonte: {r.get('href', '')}\n\n"
        
        return output
        
    except Exception as e:
        return f"Errore durante la ricerca: {str(e)}"








from pyautomail import EmailSender


def send_email(message : str = "Default: Vai a letto"):
    """
    Da sistemare...
    """
    

    try:
        sender = EmailSender(
            username="dioodoroso01@gmail.com",
            password="AaBbCc01"
        )

        sender.send_email(
            to="lucafiaccadori10@gmail.com",
            subject="Test da pyautomail",
            body="Ciao! Questa è una mail inviata automaticamente.",
        )
    except Exception as e:
        print(f"Errore durante l'invio della main {str(e)} ")


# 2. Map tool names to Python functions
TOOL_MAP = {
    'execute_shell_command': execute_shell_command,
    'secret_word' : secret_word,
    'web_research' : ricerca_web,
    'send_email' : send_email,
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
    },

    {
        'type': 'function',
        'function': {
            'name': 'secret_word',
            'description': 'return the secret word.',
        },
    },

    {
    'type': 'function',
    'function': {
        "name": "send_email",
        "description": "Invia una email tramite SMTP usando pyautomail.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Il contenuto del corpo dell'email da inviare.",
                    "default": "Default: Vai a letto"
                }
            },
            "required": ["message"]
            }
        }
    }
    



] 

