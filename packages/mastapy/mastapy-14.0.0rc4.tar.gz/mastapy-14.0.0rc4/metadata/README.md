<h1 align="center">
<img src="https://documentation.smartmt.com/MastaAPI/14.0/images/smt_logo.png" width="150" alt="SMT"><br>
<img src="https://documentation.smartmt.com/MastaAPI/14.0/images/MASTA_14_logo.png" width="400" alt="Mastapy">
</h1><br>

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Mastapy is the Python scripting API for MASTA.

- **Website**: https://www.smartmt.com/
- **Support**: https://support.smartmt.com/
- **Documentation**: https://documentation.smartmt.com/MastaAPI/14.0/


### Features

- Powerful integration with MASTA with the ability to run Python scripts from the MASTA interface directly.
- Ability to use MASTA functionality external to the MASTA software in an independent script.
- An up-to-date and tight integration with Python. This is not a lightweight wrapper around the C# API. It is specifically designed for Python and works great in tandem with other common scientific Python packages (e.g. SciPy, NumPy, Pandas, Matplotlib, Seaborn, etc.)
- Extensive backwards compatibility support. Scripts written in older versions of mastapy will still work with new versions of MASTA.
- Full support for Linux and .NET 6 versions of the MASTA API.

### Release Information

#### Major Changes

- Python.NET DLLs are now embedded in mastapy and MASTA defaults to loading them. This allows us to update supported Python versions between MASTA releases.
- Every mastapy class is now implemented as a dataclass. This has various performance and usability benefits (especially if using Python 3.10+.)
- Adds support for .NET 6 versions of the MASTA API.
- Adds Linux support.

#### Minor Changes

- Autocompletion for `mastapy` imports has been improved. Members that should be hidden from the user are no longer suggested.
- `mastapy.Examples` has been added to simplify loading example designs, e.g. `Examples.Automotive.SCOOTER_GEARBOX.load()`. More information can be found in the `Examples` class documentation.
- Replaces Black formatting with [Ruff](https://docs.astral.sh/ruff/).
- Small bug fixes and improvements.