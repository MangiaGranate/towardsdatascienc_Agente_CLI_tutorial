import ollama
llm = "qwen2.5"

from tools import TOOL_MAP, TOOLS_SCHEMA


import sys
import json
import requests

def _is_ollama_alive(verbose : bool = False):
    ''''
    Assicurati che ollama sia in esecuzione inviando una richiesta alla porta che espone in locale
    '''
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=1)
        sc = r.status_code
        if verbose: print(f"Ollama in esecuzione (status code = {sc})")
        return True
    except:
        print("Ollama non risponde in locale...")
        return False




"""
messager sarà la cronologia delle conversazioni: 
list[dict] in cui ogni dizionario rappresenta una richiesta o una risposta di uno dei 3 ruoli (user, assistance, system)
Il primo messaggio dell'elenco è da system che specifica all Agente come affrontare la conversazione.
Ogni messaggio sarà un dizionario con chiavi "role" e "content"
"""
messages = [
        {"role": "system", "content": "You are a helpful local CLI assistant. You can inspect the system and run tasks using your tools, use only occidental char"},
    ]

while _is_ollama_alive():
    try:
        user_input = input("🙂 >")
        if user_input.lower() in ['exit', 'quit']:
            break
        if not user_input.strip():
            continue

        messages.append({"role": "user", "content": user_input})
        
        # Request completion from Ollama with enabled tools
        response = ollama.chat(
            model=llm,
            messages=messages,
            tools=TOOLS_SCHEMA
        )

        # Process potential tool calls requested by the model
        while response.get('message', {}).get('tool_calls'):
            messages.append(response['message'])
            
            for tool_call in response['message']['tool_calls']:
                tool_name = tool_call['function']['name']
                arguments = tool_call['function']['arguments']
                
                print(f"🔧 >[Executing Tool] {tool_name}({json.dumps(arguments)})")
                
                if tool_name in TOOL_MAP:
                    # Execute tool and grab output string
                    tool_result = TOOL_MAP[tool_name](**arguments)
                    
                    # Provide tool outcome back to the model context
                    messages.append({
                        "role": "tool",
                        "name": tool_name,
                        "content": tool_result
                    })
                else:
                    print(f"🔧 >[TOOL ERROR] Unknown tool execution attempted: {tool_name}")
            
            # Re-submit history including tool logs for final evaluation
            response = ollama.chat(
                model=llm,
                messages=messages,
                tools=TOOLS_SCHEMA
            )


        # Display final text answer to user
        res = response['message']['content']
        print(f"👽 >{res}\n")
        messages.append({"role": "assistant", "content": res})
            

    except Exception as e:
        print(f"\n[ERROR]\t{e}")
        sys.exit(-1)