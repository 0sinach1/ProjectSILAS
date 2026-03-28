import time
import os
from voice import speak, listen
from brain import think
from actions import execute

# ── Conversation Memory ───────────────────────────
conversation_history = []

def add_to_history(role, content):
    """Add message to conversation history"""
    conversation_history.append({
        "role": role,
        "content": content
    })
    # Keep last 20 messages only
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
            
            if not user_input:
                continue
            
            # Ignore background noise transcriptions
            if len(user_input) < 5 or user_input.strip(".").strip() == "":
                continue

            # Shutdown command
            if any(word in user_input.lower() for word in ["shutdown", "goodbye", "quit", "exit", "sleep", "shot down", "close down"]):
                speak("Going offline. Stay sharp, Boss.")
                break

            # Step 2 — Add to history
            add_to_history("user", user_input)

            # Step 3 — Think
            print("Thinking...")
            response = think(conversation_history)

            # Step 4 — Extract response parts
            action = response.get("action", "answer_question")
            params = response.get("params", {})
            spoken = response.get("speak", "I didn't catch that.")

            # Step 5 — Execute action if needed
            if action != "answer_question":
                print(f"Executing: {action} with {params}")
                execute(action, params)

            # Step 6 — Speak
            speak(spoken)

            # Step 7 — Save to history
            add_to_history("assistant", spoken)

        except KeyboardInterrupt:
            speak("Going offline. Stay sharp, Boss.")
            break

        except Exception as e:
            print(f"Error in main loop: {e}")
            continue

# ── Entry Point ───────────────────────────────────
if __name__ == "__main__":
    print("=" * 40)
    print("        SILAS — Booting up...          ")
    print("=" * 40)
    run_silas()