from __future__ import annotations

from typing import Iterable, Dict, Any

from packaging.requirements import Requirement

from ._import import try_import_requirement


class Requirements:
    r"""
    Manage optional requirements and their versions at runtime.

    Examples:
        >>> r = Requirements(requirements=[Requirement("pandas==2.*"), Requirement("numpy<2")])
        >>> r.try_import(name="pandas", reason="This is required to read a CSV file.")
        Traceback (most recent call last):
          ...
        src.optional_requirements._errors.MissingRequirementError: The `pandas` Python module is not installed.
        This is required to read a CSV file.
        Required version: ==2.*
    """

    requirements: Dict[str, Requirement]

    def __init__(self, *, requirements: Iterable[Requirement]) -> None:
        self.requirements = {r.name: r for r in requirements}

    def try_import(
        self,
        *,
        name: str,
        reason: str,
    ) -> Any:
        """
        Try to import the given module. If it fails, raise `PythonModuleNotInstalled` with a user-friendly message, rather
        than `ImportError`.

        If the given module name is one of our optional requirements, check the version, and raise
        `PythonModuleIncompatibleVersion` if the available version does not meet the spec.

        Args:
            name: The name of the module to import.
            reason: A user-friendly message saying why this module is required.

        Returns:
            The module, if the import works.
        """
        return try_import_requirement(
            requirement=self.requirements.get(name, Requirement(name)),
            reason=reason,
        )
