import os
import yagmail
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("RIFT_API_KEY"),
    base_url="https://inference.cloudrift.ai/v1"
)

def get_llm_response(prompt):
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return completion.choices[0].message.content

def send_email_alert(pattern: str, prompt: str, timestamp: str):
    sender = os.getenv("ALERT_EMAIL_SENDER")
    app_password = os.getenv("ALERT_EMAIL_APP_PASSWORD")
    recipient = os.getenv("ALERT_EMAIL_RECIPIENT")
    if not all([sender, app_password, recipient]):
        print("Email alert credentials or recipient not set.")
        return
    subject = "HONEYPOT ALERT"
    body = f"Malicious activity detected on DeceptionNet!\nPattern: {pattern}\nPrompt: {prompt[:100]}\nTime: {timestamp}"
    try:
        yag = yagmail.SMTP(sender, app_password)
        yag.send(to=recipient, subject=subject, contents=body)
    except Exception as e:
        print(f"Failed to send email alert: {e}") 