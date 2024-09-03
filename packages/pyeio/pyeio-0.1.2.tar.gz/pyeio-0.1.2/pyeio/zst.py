from pathlib import Path
from typing import Callable, Generator, Any
from zstandard import ZstdDecompressor


MAX_WINDOW_SIZE: int = 1 << 31


class StreamReader:
    def __init__(
        self,
        path: str | Path,
        delimiter: bytes,
        handler: Callable[[bytes], Any] = lambda x: x,
        size: int = 1 << 20,
    ) -> None:
        self.path = path
        self.delimiter = delimiter
        self.size = size
        self.handler = handler
        self.reset()

    def reset(self) -> None:
        self.stream = ZstdDecompressor(
            max_window_size=MAX_WINDOW_SIZE,
        ).stream_reader(open(self.path, "rb"))
        self.buffer = b""
        self.chunks = []

    def __iter__(self) -> Generator[bytes, None, None]:
        while True:
            try:
                yield next(self)
            except StopIteration:
                break

    def __next__(self) -> bytes | Any:
        if len(self.chunks):
            current = self.chunks.pop(0)
            return self.handler(current)
        else:
            chunk = self.stream.read(self.size)
            if chunk:
                self.chunks = (self.buffer + chunk).split(self.delimiter)
                self.buffer = self.chunks[-1]
                self.chunks = self.chunks[:-1]
                current = self.chunks.pop(0)
                return self.handler(current)
            else:
                raise StopIteration()

    def read_chunk(self) -> bytes | Any:
        return self.__next__()

    def read_chunks(self, n: int) -> list[bytes] | list[Any]:
        return [self.read_chunk() for _ in range(n)]


def read(
    path: str | Path,
    delimiter: bytes = b"\n",
    handler: Callable[[bytes], Any] = lambda x: x,
    size: int = 1 << 20,
) -> Generator[bytes, None, None] | Generator[Any, None, None]:
    reader = StreamReader(
        path=path,
        delimiter=delimiter,
        handler=handler,
        size=size,
    )
    for chunk in reader:
        yield chunk


# def load():
#     """Decompress and load entire file into memory."""
#     raise NotImplementedError()


# def save():
#     """Compress and save serializable data to .zst file."""
#     raise NotImplementedError()


# def compress():
#     """Compress an existing file to ZST."""
#     raise NotImplementedError()


# def decompress():
#     """Decompress an existing file."""
#     raise NotImplementedError()


# from pyeio.core.types import FilePath


# def read(): ...


# def read_lines(): ...


# def compress(source: FilePath, target: FilePath): ...


# def decompress(source: FilePath, target: FilePath): ...
