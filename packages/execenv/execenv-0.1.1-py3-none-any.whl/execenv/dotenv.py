import re
from typing import Dict

LINE = re.compile(
    r'^\s*(?:export\s+)?([\w.-]+)(?:\s*=\s*?|:\s+?)(\s*\'(?:\\\'|[^\'])*\'|\s*"(?:\\"|[^"])*"|\s*`(?:\\`|[^`])*`|[^#\r\n]+)?\s*(?:#.*)?$',
    re.MULTILINE,
)


def parse(src: str):
    """
    Parse a .env file based on the rules defined in [dotenv](https://github.com/motdotla/dotenv?tab=readme-ov-file#what-rules-does-the-parsing-engine-follow).

    Ported from https://github.com/motdotla/dotenv/blob/master/lib/main.js .

    Args:
        src (str): Source multi-line string contains K-V pairs.
    """
    obj: Dict[str, str] = {}

    # Convert line breaks to same format
    src = src.replace("\r\n", "\n").replace("\r", "\n")

    matches = LINE.findall(src)
    for match in matches:
        key = match[0]

        # Default undefined or null to empty string
        value = match[1] or ""

        # Remove whitespace
        value = value.strip()

        # Check if double quoted
        maybeQuote = value[0] if value else ""

        # Remove surrounding quotes
        value = re.sub(r"^(['\"`])([\s\S]*)\1$", r"\2", value)

        # Expand newlines if double quoted
        if maybeQuote == '"':
            value = value.replace("\\n", "\n").replace("\\r", "\r")

        # Add to object
        obj[key] = value

    return obj
