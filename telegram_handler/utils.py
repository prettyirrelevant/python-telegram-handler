def escape_html(text: str) -> str:
    """Escapes all html characters in text."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
