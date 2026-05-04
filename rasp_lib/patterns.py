import re

SQLI_PATTERNS = re.compile(
    r"\b(union\s+select|select\s+.*from|insert\s+into|drop\s+table|exec\s|xp_cmdshell)\b",
    re.IGNORECASE
)

XSS_PATTERNS = re.compile(
    r"(<script[^>]*?>.*?</script>|javascript:|document\.)",
    re.IGNORECASE | re.DOTALL
)

CMD_INJECTION_PATTERNS = re.compile(
    r"(\||;|\$\(|\$\{)",
    re.IGNORECASE
)

PATH_TRAVERSAL_PATTERNS = re.compile(
    r"(\.\./|\.\.\\|/etc/passwd)",
    re.IGNORECASE
)

SECURITY_CHECKS = [
    ("SQL_INJECTION", SQLI_PATTERNS),
    ("XSS", XSS_PATTERNS),
    ("COMMAND_INJECTION", CMD_INJECTION_PATTERNS),
    ("PATH_TRAVERSAL", PATH_TRAVERSAL_PATTERNS),
]
