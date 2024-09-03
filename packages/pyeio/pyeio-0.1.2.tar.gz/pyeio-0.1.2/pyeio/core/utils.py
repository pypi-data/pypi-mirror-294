from pathlib import Path
from warnings import warn
from .types import (
    FileExtension,
    file_extensions,
    variant_file_extensions,
    variant_to_standard,
)


def parse_file_extension(path: str | Path) -> FileExtension | None:
    """
    Parse the file extension from a given file path.

    Args:
        path (FilePath): The path to the file.

    Returns:
        FileExtension: Literal str file extension.
    """
    path = Path(path)
    file_name: str = path.name
    file_name_components: list[str] = file_name.split(".")
    if not len(file_name_components):
        raise ValueError(f"Invalid file name: {file_name}")
