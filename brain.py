import anthropic
import socket
import json
from config import ANTHROPIC_API_KEY, ONLINE_MODEL, SYSTEM_PROMPT

# ── Network Detection ─────────────────────────────
def is_online():
    """Check if internet connection is available"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect(("8.8.8.8", 53))
        s.close()
        return True
    except:
        return False

# ── Claude API (Online) ───────────────────────────
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def ask_claude(conversation_history):
    """Send conversation to Claude and get response via streaming"""
    full_response = ""
    
    try:
        with client.messages.stream(
            model=ONLINE_MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=conversation_history
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text
        
        print()  # new line after streaming finishes
        return full_response
    
    except Exception as e:
        print(f"Claude error: {e}")
        return '{"action": "answer_question", "params": {}, "speak": "I encountered an error reaching my online brain. Try again."}'

# ── Ollama (Offline) ──────────────────────────────
def ask_ollama(conversation_history):
    """Send conversation to local Ollama model"""
    import requests
    
    # Format history into a single prompt for Ollama
    messages = "\n".join([
        f"{'User' if m['role'] == 'user' else 'SILAS'}: {m['content']}"
        for m in conversation_history
    ])
    
    prompt = f"{SYSTEM_PROMPT}\n\n{messages}\nSILAS:"
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
            
        )
        return response.json()["response"].strip()
    
    except Exception as e:
        print(f"Ollama error: {e}")
        return '{"action": "answer_question", "params": {}, "speak": "Offline brain is unavailable. Please check Ollama is running."}'

# ── Main Brain Function ───────────────────────────
def think(conversation_history):
    """Route to the right brain depending on connection"""
    if False:
        print("[Online — using Claude]")
        response = ask_claude(conversation_history)
    else:
        print("[Offline — using Ollama/Mistral]")
        response = ask_ollama(conversation_history)
    
    # Parse the JSON response
    try:
        start = response.find("{")
        end = response.rfind("}") + 1
        clean = response[start:end]
        data = json.loads(clean)
        return data
    
    except json.JSONDecodeError:
        # If Ollama doesn't return clean JSON, wrap it
        return {
            "action": "answer_question",
            "params": {},
            "speak": response.strip()
        }