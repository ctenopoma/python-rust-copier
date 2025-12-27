# Rust-Python Copier Template

A [Copier](https://copier.readthedocs.io/) template for scaffolding production-ready Rust-backed Python libraries on Windows with full packaging, testing, and documentation support.

## Features

- 🦀 **Rust + Python Integration**: Seamless PyO3 bindings for exposing Rust code to Python
- 📦 **Modern Python Packaging**: Uses `uv` for fast dependency management and `maturin` for building
- 🔍 **Code Quality Tools**: Pre-configured with `ruff`, `pyrefly` for Python and `clippy`, `rustfmt` for Rust
- ✅ **Testing Ready**: Integrated `pytest` for Python tests and `cargo test` for Rust
- 📚 **Documentation**: Sphinx-based documentation scaffold with automatic API generation
- 🪟 **Windows-First**: Optimized for Windows 10+ with documented macOS/Linux caveats
- 🎯 **Deterministic Builds**: Reproducible project generation with lockfile support
- ⚡ **Fast Bootstrap**: From template to working build in under 10 minutes

## Quick Start

### Prerequisites

Ensure you have the following installed on your Windows machine:

- **Python 3.10+** with pip
- **Rust 1.75+** ([rustup](https://rustup.rs/) recommended)
- **Copier 9.0+** (`pip install copier` or `pipx install copier`)
- **uv** (optional but recommended: `pip install uv`)
- **Visual Studio Build Tools** or equivalent C/C++ compiler

### Generate a New Project

```powershell
# Using Copier from GitHub
copier copy https://github.com/ctenopoma/python-rust-copier.git my-project
cd my-project

# Bootstrap the project
uv sync --group dev
uv run maturin develop

# Run tests
uv run pytest

# Build documentation
uv run sphinx-build -b html docs build/docs

# Build distributions
uv build
```

### Using the Template Locally

```powershell
# Clone this repository
git clone https://github.com/ctenopoma/python-rust-copier.git
cd python-rust-copier

# Generate from local template
copier copy template my-project
```

## Template Configuration

When you run the template, you'll be prompted for:

| Variable | Description | Default |
|----------|-------------|---------|
| `project_name` | Human-friendly project name | "My Rust-Py Library" |
| `package_name` | Python package name (PEP 8 compliant) | "mypkg" |
| `version` | Initial version (semver) | "0.1.0" |
| `author` | Author name | "" |
| `license` | SPDX license identifier | "MIT" |
| `description` | Short project description | "Rust-backed Python library template" |
| `python_version` | Target Python version | "3.12" |
| `rust_toolchain` | Rust toolchain via rustup | "stable" |
| `uv_lock` | Generate uv lockfile on scaffold | true |
| `ffi_boundary` | FFI boundary (fixed to PyO3) | "PyO3" |
| `target_platform` | Target deployment platform | "Both" |

## Generated Project Structure

```
my-project/
├── my_package/          # Python package
│   └── __init__.py      # Python module with Rust bindings import
├── src/                 # Rust source code
│   └── lib.rs           # PyO3 bindings and Rust implementations
├── tests/
│   ├── python/          # Python tests (pytest)
│   │   └── test_example.py
│   └── rust/            # Rust tests (cargo test)
│       └── lib_tests.rs
├── docs/                # Sphinx documentation
│   ├── conf.py
│   └── index.rst
├── pyproject.toml       # Python package metadata (PEP 621)
├── Cargo.toml           # Rust crate configuration
├── noxfile.py           # Task automation
├── ruff.toml            # Ruff linter configuration
├── build.ps1            # Windows build script
├── build.sh             # Unix build script (optional)
├── README.md            # Project README
├── CHANGELOG.md         # Version history
└── BUILDING.md          # Build instructions
```

## Development Workflow

### Building the Extension

```powershell
# Development mode (editable install)
uv run maturin develop

# Release build
uv run maturin build --release
```

### Running Tests

```powershell
# Python tests
uv run pytest

# Rust tests
cargo test

# Run all tests with coverage
uv run pytest --cov=my_package tests/python/
```

### Code Quality

```powershell
# Python linting
uv run ruff check .
uv run pyrefly

# Rust linting
cargo fmt -- --check
cargo clippy -- -D warnings

# Auto-fix issues
uv run ruff check --fix .
cargo fmt
```

### Building Documentation

```powershell
# Build HTML docs
uv run sphinx-build -b html docs build/docs

# Serve docs locally
cd build/docs && python -m http.server
```

## Testing This Template

This repository includes integration tests to validate the template:

```powershell
# Install test dependencies
pip install pytest copier

# Run all integration tests
python -m pytest tests/integration/ -v

# Run specific test
python -m pytest tests/integration/test_render.py -v
```

### Test Coverage

- **test_render.py**: Template rendering and determinism
- **test_scaffold.py**: Generated project structure validation
- **test_build.py**: Build pipeline (uv sync → maturin develop → uv build)
- **test_docs.py**: Documentation generation with Sphinx

## Project Architecture

### PyO3 Boundary

The template uses [PyO3](https://pyo3.rs/) to create Python bindings for Rust code:

- **Rust side** (`src/lib.rs`): Implements business logic with `#[pyfunction]` macros
- **Python side** (`package/__init__.py`): Imports and exposes native module
- **Build integration**: `maturin` handles compilation and packaging

### Error Handling

Rust errors are automatically converted to Python exceptions:

```rust
#[pyfunction]
fn validate_name(name: String) -> PyResult<String> {
    if name.trim().is_empty() {
        Err(PyValueError::new_err("name must not be empty"))
    } else {
        Ok(name)
    }
}
```

Python usage:
```python
from my_package import validate_name

try:
    validate_name("")  # Raises ValueError
except ValueError as e:
    print(f"Error: {e}")
```

## Platform Support

### Primary: Windows 10+
- Full support with optimized build scripts
- Native wheel generation
- Visual Studio Build Tools integration

### Secondary: Linux / macOS
- Supported with documented caveats
- May require additional build dependencies
- Use `build.sh` instead of `build.ps1`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines, code style, and how to submit changes.

## Versioning

This template follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes to generated project structure
- **MINOR**: New features or significant improvements
- **PATCH**: Bug fixes and minor improvements

## License

This template is released under the MIT License. Generated projects can use any license specified during generation.

## Support

- **Issues**: [GitHub Issues](https://github.com/your-org/rust-python-template/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/rust-python-template/discussions)
- **Documentation**: See [BUILDING.md](template/files/BUILDING.md.jinja) in generated projects

## Acknowledgments

Built with:
- [Copier](https://copier.readthedocs.io/) - Template engine
- [PyO3](https://pyo3.rs/) - Rust-Python bindings
- [maturin](https://www.maturin.rs/) - Build tool for Rust Python extensions
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- [ruff](https://github.com/astral-sh/ruff) - Fast Python linter
- [Sphinx](https://www.sphinx-doc.org/) - Documentation generator
