# TOWARDSDATASCIENC - TUTORIAL: agente CLI locale

Si fa riferimento al tutorial https://towardsdatascience.com/cli-agents-with-python-ollama/?utm_source=copilot.com
Il tutorial ha lo scopo di sviluppare un agente in grado di lanciare comandi shell. Verra spiegatò quali tools definire e come farli chiamare dal nostro file .py

LINUX:
``` shell
curl -fsSL https://ollama.com/install.sh | sh
```

WINDOWS:
``` shell
irm https://ollama.com/install.ps1 | iex
```

modello qwen2.5
è necessario che il modello sia installato in ollama per eseguire lo script
``` txt
ollama run qwen2.5
```

Il server Ollama deve gia essere installato in locale per poter eseguire lo script, la libreria ollama presente nel requirement serve solo per poter usare le funzioni Python. 
Il computer fisso sarà il server Ollama mentre il nostro script Python sarà il client che userà le API esposte per inviare richieste.

Per permettere al client di eseguire funzioni da terminale useremo la libreria interna "subprocess"

Quando si parla di Agents tipicamente i ruoli sono 3:

- system: colui che indica le direttive su come soddisfare la richiesta
- user: chi fa la richiesta
- assistance: chi risponde alla richiesta 
- tool: per inviare le tool_map delle funzioni tool come vedremo...

La prima istruzione da inviare al modello dovrà provenire da "system"

## While loop

Per tenere la chat viva si definisce un loop che inizia con l'input dell'utente e finisce con la risposta dell'agente. Il ciclo si ripete finche Ollama non smette di eseguire

In modo da permettere all'agente di usare i vari tool, dobbiamo dargli la possibilità anche di fornire gli argomenti adatti per ogni funzione chiamabile.


Di seguito la forma della risposta del modello alla chiamata di ollama.chat

``` txt
{
    "model": "llama3",
    "created_at": "2024-07-01T12:00:00Z",
    "message": {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {
                "function": {
                    "name": "get_weather",
                    "arguments": {
                        "city": "Mantova"
                    }
                }
            }
        ]
    },
    "done": True
}
```

Viene usato un secondo loop che continua ad eseguire finche l'agente richiede l'utilizzo di tools:
Dopo la richiesta dell'utente l'agente invia una serie di richieste d'utilizzo dei tool, finche non smette con le richieste il ciclo continua a farlo eseguire.
