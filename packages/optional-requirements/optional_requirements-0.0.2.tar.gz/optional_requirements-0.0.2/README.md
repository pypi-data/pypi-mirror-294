# optional_requirements

Manage optional requirements and their versions at runtime.

## Examples

### Managing requirements specified in a file

If you have a `requirements` file in your package (it must be included when installing the package), you can it to
manage optional dependencies.

The `find_requirements_file` function will start at the given path and search for a file matching the given name,
climbing up the directory tree until it finds a match or it goes out of a Python package (i.e., it no longer sees an
`__init__.py` file.).

```python
from pathlib import Path

from optional_requirements import (
    Requirements,
    parse_requirements_file,
    find_requirements_file,
    IncompatibleRequirementError,
    MissingRequirementError
)

r = Requirements(requirements=parse_requirements_file(
    find_requirements_file(
        start=Path(__file__),
        name="optional-requirements.txt",
    )
))

try:
    pd = r.try_import(name="pandas", reason="This is required to read a CSV file.")
except IncompatibleRequirementError as e:
    # The wrong version is installed.
    print(e.current_version)
    print(e.required_version)
    pass
except MissingRequirementError as e:
    # The requirement is not installed.
    print(e.required_version)
    pass
else:
    # Do something with the imported dependency.
    df = pd.DataFrame()
    pass

```

### Managing requirements as a group in code

```python
from optional_requirements import Requirements
from packaging.requirements import Requirement

r = Requirements(requirements=[Requirement("pandas==2.*"), Requirement("numpy<2")])
r.try_import(name="pandas", reason="This is required to read a CSV file.")
```

### Managing requirements one by one in code

```python
from optional_requirements import try_import_requirement
from packaging.requirements import Requirement

try_import_requirement(requirement=Requirement("numpy<2"), reason="Required for quick maths.")
```
