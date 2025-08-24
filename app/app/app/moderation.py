# Placeholder moderation functions
def text_is_safe(text: str) -> bool:
    banned_words = ["explicit", "nsfw"]
    return not any(b in text.lower() for b in banned_words)

def file_is_safe(file_path: str) -> bool:
    # Here you can integrate real image/video moderation later
    return True
