from pyeio.types import FilePath


def load(url: str) -> bytes: ...


def download(url: str, path: FilePath) -> None:
    """
    Download some JSON data

    Args:
        url (str): _description_
        path (FilePath): _description_
    """
