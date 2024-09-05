from importlib import import_module
from logging import getLogger
from typing import Any

from packaging.requirements import Requirement

from ._errors import MissingRequirementError, IncompatibleRequirementError
from ._module_info import get_module_info

logger = getLogger(__name__)


def try_import_requirement(
    *,
    requirement: Requirement,
    reason: str | None = None,
) -> Any:
    """
    Try to import the given Requirement. If it fails, raise `PythonModuleNotInstalled` with a user-friendly message,
    rather than `ImportError`.

    Check the Requirement version against the available module version, and raise `PythonModuleIncompatibleVersion` if
    the available version does not meet the spec.

    Args:
        requirement: The name of the module to import, and the allowable version range.
        reason: A user-friendly message saying why this module is required.

    Returns:
        The module, if the import works.
    """
    info = get_module_info(requirement.name)

    if not info["is_installed"]:
        raise MissingRequirementError(
            name=requirement.name,
            reason=reason,
            required_version=requirement.specifier,
        )

    if not info["can_import"]:
        # Something INSIDE the module is broken.
        # This is different from "not installed" or "wrong version".
        if info["import_error"]:
            raise info["import_error"]
        else:
            raise ImportError(
                f"Failed to import {requirement.name} for unknown reasons."
            )

    if info["version"] and not requirement.specifier.contains(info["version"]):
        if info["version"].is_devrelease:
            # We have a dev release of this module. Log a warning instead of raising an error.
            logger.warning(
                f"You are using a development version of {requirement.name}.\n"
                f"  Current version: {info['version']}\n"
                f"  Required version: {requirement.specifier}",
            )
        else:
            # We have the wrong version of this module.
            raise IncompatibleRequirementError(
                name=requirement.name,
                reason=reason,
                current_version=info["version"],
                required_version=requirement.specifier,
            )

    return import_module(requirement.name)
