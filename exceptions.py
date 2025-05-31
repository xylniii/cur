from typing import Self
from constants import BLOCK_SIZE
from context import Context


class UnmatchedQuotationException(Exception):
    def __init__(self: Self, index: tuple[int], context: Context):
        super().__init__(f"Unmatched quotation mark at character {index[0] + 1}:\n{"\n".join([f'\t{line}' for line in context.position_caret(tuple([i % BLOCK_SIZE for i in index])).splitlines()])}")
        self.index = index[0]
