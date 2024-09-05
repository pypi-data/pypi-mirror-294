from functools import cache
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from typing import TypedDict, Optional

from packaging.version import Version, InvalidVersion


class PythonModuleInfo(TypedDict):
    is_installed: bool
    can_import: bool
    import_error: Optional[BaseException]
    version: Optional[Version]
    path: Optional[Path]


@cache
def get_module_info(name: str) -> PythonModuleInfo:
    """
    Get info about an installed Python module, if available.
    """

    info: PythonModuleInfo = {
        "is_installed": False,
        "can_import": False,
        "import_error": None,
        "version": None,
        "path": None,
    }

    try:
        spec = find_spec(name)
    except ValueError:
        return info

    if spec is None:
        return info

    info["is_installed"] = True

    if spec.origin:
        info["path"] = Path(spec.origin).parent.resolve()

    try:
        module = import_module(name)
    except ImportError as e:
        info["import_error"] = e
        return info

    info["can_import"] = True

    if info["path"] is None and module.__file__ is not None:
        info["path"] = Path(module.__file__).parent.resolve()

    try:
        ver = import_module(f"{name}.version")
    except ImportError:
        return info

    try:
        info["version"] = Version(getattr(ver, "version"))
    except (InvalidVersion, TypeError, AttributeError):
        pass

    return info
