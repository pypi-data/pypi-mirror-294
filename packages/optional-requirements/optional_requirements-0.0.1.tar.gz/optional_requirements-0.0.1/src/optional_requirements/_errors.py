from packaging.specifiers import SpecifierSet
from packaging.version import Version


class OptionalRequirementsError(RuntimeError):
    """
    Base class for errors from this package.
    """


class IncompatibleRequirementError(OptionalRequirementsError):
    """
    Raise this when trying to access an optional requirement, but an incompatible version is installed.
    """

    name: str
    reason: str | None
    current_version: Version
    required_version: SpecifierSet

    def __init__(
        self,
        *,
        name: str,
        reason: str | None,
        current_version: Version,
        required_version: SpecifierSet,
    ) -> None:
        self.name = name
        self.reason = reason
        self.current_version = current_version
        self.required_version = required_version
        super().__init__(
            f"An incompatible version of the Python module `{name}` is installed.\n"
            f"{reason or ''}\n"
            f"Current version: {current_version}\n"
            f"Required version: {required_version}"
        )


class MissingRequirementError(OptionalRequirementsError):
    """
    Raise this when trying to access an optional requirement that is not installed.
    """

    name: str
    reason: str | None
    required_version: SpecifierSet

    def __init__(
        self,
        *,
        name: str,
        reason: str | None,
        required_version: SpecifierSet,
    ) -> None:
        self.name = name
        self.reason = reason
        self.required_version = required_version
        super().__init__(
            f"The `{name}` Python module is not installed.\n"
            f"{reason or ''}\n"
            f"Required version: {required_version}"
        )
