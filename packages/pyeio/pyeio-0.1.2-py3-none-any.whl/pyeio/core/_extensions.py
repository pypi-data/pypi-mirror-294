# from typing import Literal, Optional, cast
# from .. import exc

# # literal used for type hints and pydantic validation
# StandardExtension = Literal[
#     "jsonl",
#     "json",
#     "toml",
#     "xml",
#     "md",
#     "jpeg",
# ]

# # literal used for type hints and pydantic validation
# VariantExtension = Literal[
#     "ndjson",
#     "jsonlines",
#     "markdown",
#     "jpg",
# ]

# # set of 'standard' file extensions, recognized by official specifications
# standard_exts: set[StandardExtension] = set(
#     StandardExtension.__args__,  # type: ignore
# )

# # set of 'variant' file extensions, used anyways though not official
# variant_exts: set[VariantExtension] = set(
#     VariantExtension.__args__,  # type: ignore
# )

# # set of all file extensions covered here
# all_exts: set[str] = standard_exts.union(variant_exts)

# ext_translation: dict[VariantExtension, StandardExtension] = {
#     "ndjson": "jsonl",
#     "jsonlines": "jsonl",
#     "jpg": "jpeg",
# }


# def standardize(extension: str) -> StandardExtension:
#     if extension in standard_exts:
#         return extension
#     elif extension in variant_exts:
#         return ext_translation[extension]
#     else:
#         raise exc.UnknownExtensionError(extension=extension)


# def valid(
#     extension: str,
#     allowed: str | set[str],
#     message: Optional[str] = None,
# ) -> None:
#     """Validates expected extension."""
#     invalid = extension == allowed if isinstance(allowed, str) else extension in allowed
#     if invalid:
#         raise exc.InvalidExtensionError(
#             extension=extension, allowed=allowed, message=message
#         )

# from pathlib import Path
# from typing import Any
# from pyeio import json, jsonl, toml

# # extensions = {
# #     "json": json,
# #     "jsonl": jsonl,
# # }

# # known_extensions = {key for key in extensions.keys()}

# # alt_extensions = {
# #     "ndjson": "jsonl",
# #     "jsonlines": "jsonl",
# # }


# # auto resolution functions, likely unstable


# # todo: return result/basemodel here with info about what done
# def load(path: str | Path) -> Any:
#     """"""
#     ...


# def save(data: Any, path: str | Path): ...
