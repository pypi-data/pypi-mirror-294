import sys
import unittest
from contextlib import contextmanager, redirect_stderr
from io import StringIO
from pathlib import Path
from typing import Generator
from unittest.mock import patch, Mock

from optional_requirements import (
    try_import_requirement,
    MissingRequirementError,
    PythonModuleInfo,
    IncompatibleRequirementError,
)
from packaging.requirements import Requirement
from packaging.version import Version


class TestTryImportRequirement(unittest.TestCase):
    def test_module_exists(self) -> None:
        self.assertEqual(
            sys,
            try_import_requirement(
                requirement=Requirement("sys"),
                reason="Reasons",
            ),
        )

    def test_module_does_not_exist(self) -> None:
        with self.assertRaises(MissingRequirementError) as context:
            try_import_requirement(
                requirement=Requirement("foo29735==1.2.*"),
                reason="We need this because of reasons",
            )
        self.assertEqual(
            str(context.exception),
            "The `foo29735` Python module is not installed.\n"
            "We need this because of reasons\n"
            "Required version: ==1.2.*",
        )

    @patch("optional_requirements._import.get_module_info")
    def test_module_wrong_version(self, mock_get_module_info: Mock) -> None:
        mock_get_module_info.return_value = PythonModuleInfo(
            is_installed=True,
            can_import=True,
            import_error=None,
            version=Version("3.1.4"),
            path=Path("/foo/bar"),
        )

        with self.assertRaises(IncompatibleRequirementError) as context:
            try_import_requirement(
                requirement=Requirement("foo==2.*"),
                reason="We need this because of reasons",
            )
        self.assertEqual(
            """An incompatible version of the Python module `foo` is installed.
We need this because of reasons
Current version: 3.1.4
Required version: ==2.*""",
            str(context.exception),
        )

    @patch("optional_requirements._import.get_module_info")
    def test_module_correct_version(self, mock_get_module_info: Mock) -> None:
        mock_get_module_info.return_value = PythonModuleInfo(
            is_installed=True,
            can_import=True,
            import_error=None,
            version=Version("2.3.7"),
            path=Path("/foo/bar"),
        )

        with mock_module("foo") as foo_module:
            self.assertEqual(
                foo_module,
                try_import_requirement(
                    requirement=Requirement("foo==2.*"),
                    reason="We need this because of reasons",
                ),
            )

    @patch("optional_requirements._import.get_module_info")
    def test_module_dev_version(self, mock_get_module_info: Mock) -> None:
        """
        When a development version is detected, allow it, regardless of the version constraints, but print a warning.
        """

        mock_get_module_info.return_value = PythonModuleInfo(
            is_installed=True,
            can_import=True,
            import_error=None,
            version=Version("3.1.4.dev0+g617aac6.d20230906"),
            path=Path("/foo/bar"),
        )

        with mock_module("foo") as foo_module:
            stderr = StringIO()
            with redirect_stderr(stderr):
                result = try_import_requirement(
                    requirement=Requirement("foo==2.*"),
                    reason="We need this because of reasons",
                )

            self.assertEqual(foo_module, result)
            self.assertEqual(
                "You are using a development version of foo.\n"
                "  Current version: 3.1.4.dev0+g617aac6.d20230906\n"
                "  Required version: ==2.*",
                stderr.getvalue().strip(),
            )

    @patch("optional_requirements._import.get_module_info")
    def test_module_import_error(self, mock_get_module_info: Mock) -> None:
        import_error = Exception("Something went wrong")

        mock_get_module_info.return_value = PythonModuleInfo(
            is_installed=True,
            can_import=False,
            import_error=import_error,
            version=None,
            path=None,
        )

        with self.assertRaises(Exception) as context:
            try_import_requirement(
                requirement=Requirement("foo==2.*"),
                reason="We need this because of reasons",
            )
        self.assertEqual(import_error, context.exception)

    @patch("optional_requirements._import.get_module_info")
    def test_module_unknown_import_error(self, mock_get_module_info: Mock) -> None:
        mock_get_module_info.return_value = PythonModuleInfo(
            is_installed=True,
            can_import=False,
            import_error=None,
            version=None,
            path=None,
        )

        with self.assertRaises(Exception) as context:
            try_import_requirement(
                requirement=Requirement("foo==2.*"),
                reason="We need this because of reasons",
            )
        self.assertEqual(
            repr(ImportError("Failed to import foo for unknown reasons.")),
            repr(context.exception),
        )


@contextmanager
def mock_module(name: str) -> Generator[Mock, None, None]:
    """
    Temporarily create a fake module that can be imported.
    """
    module = Mock()

    original = sys.modules.get(name)

    try:
        sys.modules[name] = module
        yield module
    finally:
        if original:
            sys.modules[name] = original
        else:
            del sys.modules[name]
