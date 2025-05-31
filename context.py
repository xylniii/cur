from dataclasses import dataclass
from typing import Self

@dataclass
class Context:
    content: str
    starting_index: int
    ending_index: int

    def cut(text: str, middle: tuple[int], size: int) -> tuple[str, int, int]:
        length = len(text)
        if length == 0 or not 0 <= middle[0] <= length or not 0 <= middle[1] <= length:
            raise IndexError("Parameter index out of range.")
        size_left = size
        size_right = size
        if middle[0] - size_left < 0:
            size_left = middle[0]
        if middle[1] + size_right >= length:
            size_right = length - middle[1]
        return (text[middle[0] - size_left:middle[1]] + text[middle[1]:middle[1] + size_right], (middle[0] - size_left), (middle[1] + size_right - 1))


    def position_caret(self: Self, highlight: tuple[int]) -> str:
        starting_index = self.starting_index
        ending_index = self.ending_index
        if not starting_index <= highlight[0] <= ending_index or not starting_index <= highlight[1] <= ending_index + 1:
            raise IndexError(f"{highlight[0]}–{highlight[1]} is out of bounds of [{starting_index}, {ending_index}]")
        return f"...{self.content}...\n{" " * (highlight[0] - starting_index + 3)}{"^" * (highlight[1] - highlight[0])}"
