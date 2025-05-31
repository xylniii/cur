#!/usr/bin/env python3
import sys
from clipboard import get_clipboard_text, paste_clipboard_text
from files import File
from text import Text

def main(argv: list[str]) -> int:
    try:
        if len(argv) > 1:
            print("Usage: ./main.py [FILE]")
        elif len(argv) == 1:
            text = Text(File(argv[0]))
            text.clean_up()
            text.match_quotes()
            print("Text has been successfully cleaned.")
        else:
            text = Text(get_clipboard_text())
            text.clean_up()
            text.match_quotes()
            paste_clipboard_text(text)
            print("Text has been succesfully cleaned.")
    except Exception as err:
        print(err)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
