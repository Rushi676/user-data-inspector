import pyperclip

def get_clipboard_content():
    try:
        content = pyperclip.paste()
        return content if content else None
    except Exception as e:
        print(f"Error reading clipboard: {e}")
        return None
