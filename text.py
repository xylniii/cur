from dataclasses import dataclass
from typing import Self
from change import Change
from constants import BLOCK_SIZE
from context import Context
from exceptions import UnmatchedQuotationException
from files import File

@dataclass
class Text:
    contents: str | File # either the actual contents or a filepath

    def clean_up(self: Self):
        mapping = {
            "'s ": "’s ",
            "s' ": "s’ ",
            "_": "‐",
            "--": "—",
            "n't": "n’t",
            " —": "—",
            "— ": "—",
            " — ": "—",
        }
        if isinstance(self.contents, str):
            contents = self.contents
            for key in mapping:
                contents = contents.replace(key, mapping[key])
            self.contents = contents
        else:
            contents = self.contents.contents()
            while True:
                try:
                    text = next(contents)
                    for key in mapping:
                        text = text.replace(key, mapping[key])
                    self.contents.send(text)
                except StopIteration:
                    self.contents.write()
                    break

    def match_quotes(self: Self):
        quote_stack = []
        changes: list[Change] = []
        if isinstance(self.contents, str):
            text = self.contents
            for index, char in enumerate(text):
                if char == '"':
                    if '“' not in quote_stack:
                        changes.append(Change('“', index, index + 1))
                        quote_stack.append('“')
                    else:
                        changes.append(Change('”', index, index + 1))
                        if quote_stack[-1] == '“':
                            quote_stack.pop()
                        else:
                            index = changes[-2].get_bounds()
                            raise UnmatchedQuotationException(index, Context(*Context.cut(text, index, 45)))
                if char == "'":
                    if '‘' not in quote_stack:
                        changes.append(Change('‘', index, index + 1))
                        quote_stack.append('‘')
                    else:
                        changes.append(Change('’', index, index + 1))
                        if quote_stack[-1] == '‘':
                            quote_stack.pop()
                        else:
                            index = changes[-2].get_bounds()
                            raise UnmatchedQuotationException(index, Context(*Context.cut(text, index, 45)))
            if len(quote_stack) == 1:
                index = changes[-1].get_bounds()
                raise UnmatchedQuotationException(index, Context(*Context.cut(text, index, 45)))
            text = list(text)
            for change in changes:
                change.apply_to(text)
            self.contents = "".join(text)
        else:
            count = 0
            contents = self.contents.contents()
            while True:
                try:
                    text = next(contents)
                    for index, char in enumerate(text):
                        if char == '"':
                            if '“' not in quote_stack:
                                changes.append(Change('“', index, index + 1))
                                quote_stack.append('“')
                            else:
                                changes.append(Change('”', index, index + 1))
                                if quote_stack[-1] == '“':
                                    quote_stack.pop()
                                else:
                                    index = changes[-2].get_bounds()
                                    raise UnmatchedQuotationException(tuple([i + (count * BLOCK_SIZE) for i in index]), Context(*Context.cut(text, index, 45)))
                        if char == "'":
                            if '‘' not in quote_stack:
                                changes.append(Change('‘', index, index + 1))
                                quote_stack.append('‘')
                            else:
                                changes.append(Change('’', index, index + 1))
                                if quote_stack[-1] == '‘':
                                    quote_stack.pop()
                                else:
                                    index = changes[-2].get_bounds()
                                    raise UnmatchedQuotationException(tuple([i + (count * BLOCK_SIZE) for i in index]), Context(*Context.cut(text, index, 45)))
                    text = list(text)
                    for change in changes[:-1]:
                        change.apply_to(text)
                    if len(quote_stack) == 0:
                        for change in changes:
                            change.apply_to(text)
                    self.contents.send("".join(text))
                    count += 1
                except StopIteration:
                    if len(quote_stack) == 1:
                        index = changes[-1].get_bounds()
                        if isinstance(text, list):
                            text = "".join(text)
                        raise UnmatchedQuotationException(tuple([i + (count * BLOCK_SIZE) for i in index]), Context(*Context.cut(text, index, 45)))
                    self.contents.write()
                    break
