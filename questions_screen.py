
import requests

def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)
    return response.json()["response"]

answer = ask_ollama(" give me finance situations for teenagers and ask the user  question about them")
ask_ollama(answer)

