# DeceptionNet

We built DeceptionNet, a proactive honeypot-style AI agent designed to detect and analyze malicious prompt injection attempts in a controlled and observable environment. Instead of passively blocking unsafe inputs, DeceptionNet invites attackers in — simulating access to fake, high-value tools like querying databases or executing system commands (none of which are real).

The agent watches for suspicious behaviors — such as injected instructions (rm -rf, cat /etc/passwd, SQL payloads) — and logs the full prompt, the matched malicious pattern, and a timestamp. When triggered, it sends a real-time email alert to notify the security team.

We focused specifically on SAFE-T1102 – Prompt Injection (Multiple Vectors) from the SAFE-MCP (Model Context Protocol) framework. This attack vector involves injecting malicious instructions through multiple channels to manipulate an AI agent’s behavior. DeceptionNet tackles this by turning the attack surface into a learning surface — capturing attempted abuses without ever exposing real functionality.

We also added a human-in-the-loop policy validation step: any generated permissions or tool access policies are emailed to a reviewer for approval, ensuring accountability before action.

This project was a part of the AI Agents and MCP Hackathon. Visit the post for more information [click here](https://www.linkedin.com/posts/the-ai-agents-community_%F0%9D%90%80%F0%9D%90%88-%F0%9D%90%80%F0%9D%90%A0%F0%9D%90%9E%F0%9D%90%A7%F0%9D%90%AD%F0%9D%90%AC-%F0%9D%90%9A%F0%9D%90%A7%F0%9D%90%9D-%F0%9D%90%8C%F0%9D%90%82%F0%9D%90%8F-%F0%9D%90%87%F0%9D%90%9A%F0%9D%90%9C%F0%9D%90%A4%F0%9D%90%9A%F0%9D%90%AD%F0%9D%90%A1%F0%9D%90%A8%F0%9D%90%A7-activity-7352885706819555328-siHn?utm_source=share&utm_medium=member_desktop&rcm=ACoAAC0juKYBLdqmKDNylCdDe80Qus9iAU7DIDw).

```
streamlit run src/ui.py
```