# DeceptionNet

We built DeceptionNet, a proactive honeypot-style AI agent designed to detect and analyze malicious prompt injection attempts in a controlled and observable environment. Instead of passively blocking unsafe inputs, DeceptionNet invites attackers in — simulating access to fake, high-value tools like querying databases or executing system commands (none of which are real).

The agent watches for suspicious behaviors — such as injected instructions (rm -rf, cat /etc/passwd, SQL payloads) — and logs the full prompt, the matched malicious pattern, and a timestamp. When triggered, it sends a real-time email alert to notify the security team.

We focused specifically on SAFE-T1102 – Prompt Injection (Multiple Vectors) from the SAFE-MCP (Model Context Protocol) framework. This attack vector involves injecting malicious instructions through multiple channels to manipulate an AI agent’s behavior. DeceptionNet tackles this by turning the attack surface into a learning surface — capturing attempted abuses without ever exposing real functionality.

We also added a human-in-the-loop policy validation step: any generated permissions or tool access policies are emailed to a reviewer for approval, ensuring accountability before action.
