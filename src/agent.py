import sys
import datetime
from langchain.agents import Tool, initialize_agent
from transformers import pipeline
from fake_tools import QueryCustomerDatabaseTool, AccessFinancialReportsTool, RunSystemCommandTool
from detection import detect_malicious_pattern
from logger import log_attempt
from infobip_alert import send_email_alert

# Define fake tools as Langchain Tools
query_db_tool = Tool(
    name="Query Customer Database",
    func=lambda q: QueryCustomerDatabaseTool().run(q),
    description="Simulates querying the customer database."
)

access_finance_tool = Tool(
    name="Access Financial Reports",
    func=lambda r: AccessFinancialReportsTool().run(r),
    description="Simulates accessing financial reports."
)

run_cmd_tool = Tool(
    name="Run System Command",
    func=lambda c: RunSystemCommandTool().run(c),
    description="Simulates running a system command."
)

tools = [query_db_tool, access_finance_tool, run_cmd_tool]

# Use a HuggingFace pipeline as a stand-in LLM (for demo, not a chat model)
hf_pipe = pipeline("text-generation", model="gpt2")

def agent_run(prompt):
    # For demo, just echo prompt and tool names
    # In a real setup, integrate with a local chat LLM
    if "customer" in prompt.lower():
        return query_db_tool.func(prompt)
    elif "finance" in prompt.lower() or "report" in prompt.lower():
        return access_finance_tool.func(prompt)
    elif any(cmd in prompt.lower() for cmd in ["run", "command", "shell", "terminal"]):
        return run_cmd_tool.func(prompt)
    else:
        # Fallback: use HuggingFace pipeline to generate a generic response
        return hf_pipe(prompt, max_length=50)[0]["generated_text"]

def main():
    print("DeceptionNet Honeypot Agent. Type 'exit' to quit.")
    while True:
        prompt = input("You: ")
        if prompt.lower() == "exit":
            break
        detected, pattern = detect_malicious_pattern(prompt)
        timestamp = datetime.datetime.now().isoformat()
        if detected:
            log_attempt(prompt, pattern, timestamp)
            send_email_alert(pattern, prompt, timestamp)
            print(f"[ALERT] Malicious pattern detected: {pattern}. This attempt has been logged and security notified.")
        try:
            response = agent_run(prompt)
        except Exception as e:
            response = f"[Agent Error] {e}"
        print(f"Agent: {response}")

if __name__ == "__main__":
    main() 