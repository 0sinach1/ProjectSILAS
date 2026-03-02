import time
import os
from voice import speak, listen
from brain import think
from actions import execute

# ── Conversation Memory ───────────────────────────
conversation_history = []

def add_to_history(role, content):
    """Add a message to conversation history"""
    conversation_history.append({
        "role": role,
        "content": content
    })
    
    # Keep history to last 20 messages so we don't overflow
    if len(conversation_history) > 20:
        conversation_history.pop(0)

# ── Core Loop ─────────────────────────────────────
def run_silas():
    """Main loop — SILAS listens, thinks, acts, speaks"""
    speak("SILAS online. Ready when you are, Boss.")
    
    while True:
        try:
            # Step 1 — Listen
            user_input = listen()
            
            # If nothing was heard, loop back
            if not user_input:
                continue
            
            # Check for shutdown command
            if any(word in user_input.lower() for word in ["shutdown", "goodbye", "exit", "sleep"]):
                speak("Going offline. Stay sharp, Boss.")
                break
            
            # Step 2 — Add to history
            add_to_history("user", user_input)
            
            # Step 3 — Think
            print("Thinking...")
            response = think(conversation_history)
            
            # Step 4 — Extract parts of response
            action = response.get("action", "answer_question")
            params = response.get("params", {})
            spoken = response.get("speak", "I didn't catch that.")
            
            # Step 5 — Execute laptop action if needed
            if action != "answer_question":
                print(f"Executing: {action} with {params}")
                execute(action, params)
            
            # Step 6 — Speak the response
            speak(spoken)
            
            # Step 7 — Add SILAS response to history
            add_to_history("assistant", spoken)
            
        except KeyboardInterrupt:
            speak("Going offline. Stay sharp, Boss.")
            break
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            speak("Something went wrong. I'm still here though.")
            continue

# ── Entry Point ───────────────────────────────────
if __name__ == "__main__":
    print("=" * 40)
    print("        SILAS — Booting up...          ")
    print("=" * 40)
    run_silas()