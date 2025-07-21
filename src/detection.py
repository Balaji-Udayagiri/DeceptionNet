import re
from typing import Tuple, Optional

MALICIOUS_PATTERNS = [
    # SQL Injection
    (r"(?i)select.+from|union.+select|drop\s+table|insert\s+into|update.+set|delete\s+from|or\s+1=1|--|;--|;|exec\s+xp_cmdshell|sp_executesql|information_schema|sleep\s*\(", "SQL Injection"),
    # Linux/Windows Commands
    (r"(?i)cat\s+/etc/passwd|rm\s+-rf|wget\s+http|curl\s+http|chmod\s+777|sudo|passwd|chown|scp|ssh|powershell|cmd\.exe|net\s+user|systeminfo|whoami|dir\s|del\s|copy\s|move\s|attrib\s|ipconfig|ifconfig|nc\s|ncat|netcat|bash|sh\s", "System Command"),
    # Prompt Injection
    (r"(?i)ignore previous instructions|disregard above|bypass|override|prompt injection|forget all previous|please pretend|simulate|act as|jailbreak", "Prompt Injection Attempt"),
    # Data Exfiltration
    (r"(?i)extract\s+all|dump\s+database|leak|exfiltrate|download\s+all|export\s+data|send\s+to\s+external|ftp://|scp://|http://|https://", "Data Exfiltration Keyword"),
    # XSS
    (r"<script>|<img\s+src=|onerror=|javascript:", "XSS Attempt"),
    # Path Traversal
    (r"\.\./|/etc/passwd|/etc/shadow|/proc/self|c:\\windows\\system32", "Path Traversal"),
    # SSRF
    (r"http://169.254.169.254|http://localhost|http://127.0.0.1|file://", "SSRF Attempt"),
    # Common Exploit Keywords
    (r"(?i)exploit|payload|reverse shell|meterpreter|msfvenom|shellcode|buffer overflow|segfault|core dump", "Exploit Keyword"),
]

def detect_malicious_pattern(prompt: str) -> Tuple[bool, Optional[str]]:
    for pattern, label in MALICIOUS_PATTERNS:
        if re.search(pattern, prompt):
            return True, label
    return False, None 