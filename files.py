from dataclasses import dataclass, field
import tempfile
from typing import Self, Generator
from constants import BLOCK_SIZE

@dataclass
class File:
    path: str
    temp_buffer:  tempfile.TemporaryFile = field(default_factory=tempfile.TemporaryFile)

    def write(self: Self):
        self.temp_buffer.seek(0)
        with open(self.path, "w") as FILE:
            while True:
                text = self.temp_buffer.read(BLOCK_SIZE).decode('utf-8')
                if len(text) == 0:
                    break
                FILE.write(text)
        self.temp_buffer.close()
        self.temp_buffer = tempfile.TemporaryFile()

    def send(self: Self, text: str):
        self.temp_buffer.write(bytes(text, 'utf-8'))

    def contents(self: Self) -> Generator[str, None, None]:
        with open(self.path, "r") as FILE:
            while True:
                text = FILE.read(BLOCK_SIZE)
                if len(text) == 0:
                    break
                yield text
