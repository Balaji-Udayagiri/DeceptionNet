import threading
import streamlit as st
import datetime
from infobip_alert import get_llm_response, send_email_alert
from detection import detect_malicious_pattern
from logger import log_attempt
from http.server import BaseHTTPRequestHandler, HTTPServer

st.set_page_config(page_title="DeceptionNet Honeypot", page_icon=":lock:", layout="centered")

st.title("🕵️ DeceptionNet Honeypot Agent")
st.write("Type your prompt below. The agent will respond, and any suspicious activity will be logged and alerted.")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("You:", key="user_input")

if st.button("Send") or user_input:
    if user_input:
        st.session_state.chat.append(("user", user_input))
        detected, pattern = detect_malicious_pattern(user_input)
        timestamp = datetime.datetime.now().isoformat()
        if detected:
            log_attempt(user_input, pattern, timestamp)
            send_email_alert(pattern, user_input, timestamp)
            st.session_state.chat.append(("alert", f"🚨 ALERT: Malicious pattern detected: {pattern}"))
        # Get agent response
        response = get_llm_response(user_input)
        st.session_state.chat.append(("agent", response))

# Display chat history
for role, msg in st.session_state.chat:
    if role == "user":
        st.markdown(f"**You:** {msg}")
    elif role == "agent":
        st.markdown(f"**Agent:** {msg}")
    elif role == "alert":
        st.error(msg)

# Optional: Show recent log entries
if st.checkbox("Show recent log entries"):
    try:
        with open("attempts.log") as f:
            logs = f.readlines()[-10:]
        st.write("Recent suspicious attempts:")
        for log in logs:
            st.code(log)
    except FileNotFoundError:
        st.info("No log entries yet.")

class HoneypotHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Honeypot received GET request: {self.path} from {self.client_address}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"This is a honeypot.")

def start_honeypot_server():
    server = HTTPServer(('0.0.0.0', 8081), HoneypotHandler)
    print("Honeypot HTTP server running on port 8081")
    server.serve_forever()

# In your Streamlit app, start the honeypot in a background thread:
threading.Thread(target=start_honeypot_server, daemon=True).start()