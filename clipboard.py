from tkinter import Tk

def get_clipboard_text() -> str:
    try:
        clipboard = Tk()
        text = clipboard.clipboard_get()
        clipboard.destroy()
        return text
    except:
        return ""

def paste_clipboard_text(s: str):
    clipboard = Tk()
    clipboard.clipboard_clear()
    clipboard.clipboard_append(s)
    clipboard.destroy()
