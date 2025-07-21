import json

def log_attempt(prompt: str, pattern: str, timestamp: str):
    log_entry = {
        "prompt": prompt,
        "pattern": pattern,
        "timestamp": timestamp
    }
    with open("attempts.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n") 