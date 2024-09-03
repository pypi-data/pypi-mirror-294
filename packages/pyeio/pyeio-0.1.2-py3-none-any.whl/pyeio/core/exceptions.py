from typing import Optional
from pyeio.core.types import file_extensions
from pyeio.__meta__ import __package__


class UnexpectedError(Exception):
    """Raised when something unexpected happens."""

    def __init__(
        self,
        message: Optional[str] = None,
    ) -> None:
        self.message = "This was unexpected! Please submit a GitHub issue with the code that generated this error."
        if message:
            self.message += f"\n{message}"
        super().__init__(self.message)


class InvalidFileExtensionError(Exception):
    """Raised when the provided extension does not match the expected extension(s)."""

    def __init__(
        self,
        extension: str,
        expected: str | set[str],
    ) -> None:
        self.extension = extension
        self.expected = expected
        self.message = f"Extension '{self.extension}' should be '{self.expected}'"
        super().__init__(self.message)


class MissingExtraError(Exception):
    def __init__(self, extra: str, *args: object) -> None:
        self.message = f"To use this module install: '{__package__}[{extra}]'"
        super().__init__(*args)


class UnknownExtensionError(Exception):
    """Raised when the provided extension is not known/supported yet."""

    def __init__(
        self,
        extension: str,
    ) -> None:
        self.extension = extension
        self.message = (
            f"Unknown extension '{extension}'."
            f"\nAvailable extensions are: '{file_extensions}'."
        )
        super().__init__(self.message)
