from dataclasses import dataclass
from typing import Self

@dataclass
class Change:
    contents: str
    starting_index: int
    ending_index: int

    def get_bounds(self: Self) -> tuple[int]:
        return (self.starting_index, self.ending_index)

    def apply_to(self: Self, text: str|list[str]) -> str:
        contents = self.contents
        starting_index = self.starting_index
        ending_index = self.ending_index
        if len(contents) + (len(text) - (ending_index - starting_index)) == len(text) and isinstance(text, list):
            for index, char in enumerate(self.contents):
                text[starting_index + index] = char
            return text
        return text[0:self.starting_index] + self.contents + text[self.ending_index:]
