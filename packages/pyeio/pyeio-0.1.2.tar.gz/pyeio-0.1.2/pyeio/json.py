from pathlib import Path
from typing import TypeVar, Generator, Optional
from pyeio import txt
from pyeio.core.exceptions import InvalidFileExtensionError, MissingExtraError

try:
    import orjson
except ImportError:
    raise MissingExtraError("json")


T = TypeVar("T", bound="JSON")
JSON = bool | int | float | str | list[T] | dict[str, T]


def parse(data: str | bytes) -> JSON:
    return orjson.loads(data)


def dump(data: JSON) -> str:
    return orjson.dumps(data).decode()


def load(path: str | Path) -> JSON:
    return parse(txt.load(path=Path(path)))


def save(data: JSON, path: str | Path, overwrite: bool = False) -> None:
    path = Path(path)
    file_extension = path.name.split(".")[-1]
    if file_extension.lower() != "json":
        raise InvalidFileExtensionError(extension=file_extension, expected="json")
    txt.save(data=dump(data), path=path, overwrite=overwrite)


def walk(path: str | Path) -> Generator[tuple[str, JSON], None, None]:
    for file in Path(path).glob("**/*.json"):
        yield (str(file.absolute()), load(file))


# def get(url: str) -> JSON:
#     raise NotImplementedError()

# def download(url: str, path: str | Path):
#     raise NotImplementedError()


# def crawl(): ...
# # # todo: get recursive from webpage or online directory
# # # webpage: eg - scrape all json links and download to local dir
# # # dir: eg - s3 bucket, dl all
