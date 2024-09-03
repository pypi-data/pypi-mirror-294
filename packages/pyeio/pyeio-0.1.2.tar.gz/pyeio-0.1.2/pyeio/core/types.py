from typing import Literal, get_args

FileExtension = Literal[
    "json",
    "jsonl",
    # "toml",
    # "yaml",
    # "xml",
    # "md",
    # "jpeg",
    # "zst",
    # "nc",
]

file_extensions: tuple[str, ...] = get_args(FileExtension)


VariantFileExtension = Literal[
    "ndjson",
    "jsonlines",
    # "jpg",
    # "yml",
    # "markdown",
]


variant_file_extensions: tuple[str, ...] = get_args(VariantFileExtension)

MimeType = Literal[
    "application/json",
    "application/jsonl",
    # "application/netcdf",
    # "application/x-netcdf",
]


variant_to_standard: dict[VariantFileExtension, FileExtension] = {
    "ndjson": "jsonl",
    "jsonlines": "jsonl",
    # "jpg": "jpeg",
    # "yml": "yaml",
    # "markdown": "md",
}
