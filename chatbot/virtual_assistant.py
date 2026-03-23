"""
Virtual Assistant / Chatbot
Features:
  1. Rule-based pattern matching chatbot
  2. Wikipedia knowledge lookup
  3. Wolfram Alpha computation (API key required)
  4. Sentiment-aware responses

Install: pip install wikipedia wolframalpha
"""
import re
import random

# ─── Pattern-Response Rules ──────────────────────────────────────────
RULES = [
    (r'hi|hello|hey',                  ["Hello! How can I help you?", "Hi there! What's on your mind?", "Hey! How are you?"]),
    (r'how are you',                   ["I'm doing great, thanks for asking!", "All systems running perfectly!"]),
    (r'what is your name',             ["I'm PyBot, your AI assistant!", "My name is PyBot."]),
    (r'who made you',                  ["I was created using Python!", "A Python developer built me."]),
    (r'bye|goodbye|exit|quit',         ["Goodbye! Have a great day!", "See you later!", "Bye! Take care!"]),
    (r'thank you|thanks',              ["You're welcome!", "Happy to help!", "Anytime!"]),
    (r'what time is it',               ["__TIME__"]),
    (r'what.*date|today.*date',        ["__DATE__"]),
    (r'tell me a joke',                ["Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                                        "What do you call a fish without eyes? A fsh! 🐟"]),
    (r'what can you do',               ["I can answer questions, tell jokes, search Wikipedia, and compute with Wolfram Alpha!"]),
    (r'(.*)(weather)(.*)',             ["I can't check weather directly. Try weather.com!"]),
    (r'calculate|compute|what is (\d+[\+\-\*\/]\d+)', ["__CALC__"]),
]

def rule_based_response(user_input):
    import datetime
    lower = user_input.lower()
    for pattern, responses in RULES:
        if re.search(pattern, lower):
            response = random.choice(responses)
            if response == "__TIME__":
                return f"Current time: {datetime.datetime.now().strftime('%H:%M:%S')}"
            if response == "__DATE__":
                return f"Today is: {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
            if response == "__CALC__":
                try:
                    expr = re.findall(r'[\d\+\-\*\/\.\s]+', user_input)
                    if expr:
                        result = eval(expr[0].strip())
                        return f"Result: {result}"
                except:
                    return "I couldn't compute that."
            return response
    return None

# ─── Wikipedia Search ─────────────────────────────────────────────────
def search_wikipedia(query):
    try:
        import wikipedia
        wikipedia.set_lang("en")
        result = wikipedia.summary(query, sentences=2)
        return f"📚 Wikipedia: {result}"
    except ImportError:
        return "[Wikipedia] Run: pip install wikipedia"
    except Exception as e:
        return f"[Wikipedia] Couldn't find info on '{query}'. Try a different query."

# ─── Wolfram Alpha ────────────────────────────────────────────────────
def query_wolfram(query, app_id="DEMO"):
    try:
        import wolframalpha
        if app_id == "DEMO":
            return "🔢 Wolfram Alpha: (Add your API key from wolframalpha.com to enable computation)"
        client = wolframalpha.Client(app_id)
        res = client.query(query)
        answer = next(res.results).text
        return f"🔢 Wolfram Alpha: {answer}"
    except ImportError:
        return "[Wolfram] Run: pip install wolframalpha"
    except StopIteration:
        return "Wolfram Alpha couldn't find an answer."
    except Exception as e:
        return f"[Wolfram] Error: {e}"

# ─── Main Chatbot Loop ────────────────────────────────────────────────
def chatbot():
    print("=" * 55)
    print("      PyBot — Virtual Assistant")
    print("  Commands: 'wiki <topic>' | 'wolfram <query>' | 'quit'")
    print("=" * 55)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nPyBot: Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower().startswith("wiki "):
            query = user_input[5:]
            print(f"PyBot: {search_wikipedia(query)}")

        elif user_input.lower().startswith("wolfram "):
            query = user_input[8:]
            WOLFRAM_APP_ID = "DEMO"  # Replace with your key
            print(f"PyBot: {query_wolfram(query, WOLFRAM_APP_ID)}")

        elif user_input.lower() in ('quit', 'exit', 'bye'):
            print("PyBot: Goodbye! Have a great day! 👋")
            break

        else:
            response = rule_based_response(user_input)
            if response:
                print(f"PyBot: {response}")
            else:
                # Fall back to Wikipedia
                print(f"PyBot: Let me search Wikipedia for that...")
                print(f"PyBot: {search_wikipedia(user_input)}")

def demo_run():
    print("=== Chatbot Demo (Non-interactive) ===\n")
    test_inputs = [
        "Hello!",
        "What is your name?",
        "Tell me a joke",
        "What time is it?",
        "wiki Python programming",
        "wolfram What is the speed of light?",
        "Thank you",
        "Goodbye"
    ]
    for inp in test_inputs:
        print(f"You  : {inp}")
        if inp.lower().startswith("wiki "):
            print(f"PyBot: {search_wikipedia(inp[5:])}")
        elif inp.lower().startswith("wolfram "):
            print(f"PyBot: {query_wolfram(inp[8:])}")
        else:
            response = rule_based_response(inp) or "I'm not sure about that. Try 'wiki <topic>'."
            print(f"PyBot: {response}")
        print()

if __name__ == "__main__":
    import sys
    if "--demo" in sys.argv or True:   # Always run demo for lab purposes
        demo_run()
    # Uncomment below for interactive mode:
    # chatbot()
