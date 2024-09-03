from pathlib import Path


# text
def load(path: str | Path) -> str:
    with open(path) as file:
        data = file.read()
    file.close()
    return data


def save(data: str, path: str | Path, overwrite: bool = False) -> None:
    path = Path(path)
    if path.exists() and (not overwrite):
        raise FileExistsError(str(path))
    with open(path, "w") as file:
        file.write(data)
    file.close()


# def save_text(text: str, path: str | Path) -> None:
#     with open(path, "w") as file:


def load_text_lines(): ...


def save_text_lines(): ...


def stream_text(): ...


def stream_text_lines(): ...


def stream_text_chars(): ...


def stream_text_segments():
    """set start and end delimiters and stream the text between these"""
    ...


# binary
def load_binary(): ...


def save_binary(): ...
