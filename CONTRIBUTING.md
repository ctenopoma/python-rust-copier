# Contributing to Rust-Python Copier Template

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Commit Guidelines](#commit-guidelines)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

This project follows a professional code of conduct:

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Python 3.10+** with pip
- **Rust 1.75+** ([rustup](https://rustup.rs/))
- **Copier 9.0+** (`pipx install copier`)
- **Git** for version control
- **Visual Studio Build Tools** (Windows) or equivalent C/C++ compiler

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork:
   ```powershell
   git clone https://github.com/YOUR-USERNAME/rust-python-template
   cd rust-python-template
   ```
3. Add upstream remote:
   ```powershell
   git remote add upstream https://github.com/original-org/rust-python-template
   ```

## Development Setup

### Install Development Dependencies

```powershell
# Install Python dependencies
pip install pytest copier

# Verify Rust installation
rustc --version
cargo --version

# Verify Copier installation
copier --version
```

### Project Structure

```
rust-python-template/
├── template/               # Copier template files
│   ├── copier.yaml        # Template configuration
│   ├── files/             # Template files to be rendered
│   │   ├── *.jinja        # Jinja2 templates
│   │   └── {{ package_name }}/  # Dynamic directory names
│   └── hooks/             # Post-generation hooks
├── tests/                 # Integration tests
│   └── integration/       # Template validation tests
├── specs/                 # Feature specifications
│   └── 001-rust-python-copier-template/
├── .specify/              # Project automation
└── ci/                    # CI/CD workflows
```

## Making Changes

### Branching Strategy

- `main` - Stable release branch
- `develop` - Development branch (if used)
- `feature/###-description` - Feature branches
- `fix/description` - Bug fix branches

### Working on a Feature

1. Create a feature branch:
   ```powershell
   git checkout -b feature/add-new-option
   ```

2. Make your changes in the appropriate location:
   - **Template files**: `template/files/`
   - **Template config**: `template/copier.yaml`
   - **Post-gen hooks**: `template/hooks/`
   - **Tests**: `tests/integration/`
   - **Documentation**: Root `README.md` or template docs

3. Test your changes locally:
   ```powershell
   # Test template rendering
   copier copy template ../test-output --trust
   
   # Run integration tests
   python -m pytest tests/integration/ -v
   ```

## Testing

### Running Tests

```powershell
# Run all integration tests
python -m pytest tests/integration/ -v

# Run specific test file
python -m pytest tests/integration/test_render.py -v

# Run with detailed output
python -m pytest tests/integration/ -v -s

# Run specific test
python -m pytest tests/integration/test_build.py::test_build_pipeline -v
```

### Test Structure

- **test_render.py**: Template rendering validation
  - Default answers rendering
  - Deterministic output verification
  
- **test_scaffold.py**: Generated project structure validation
  - File existence checks
  - Content validation
  - Metadata propagation
  
- **test_build.py**: Build pipeline validation
  - `uv sync` dependency installation
  - `maturin develop` extension building
  - `uv build` distribution creation
  
- **test_docs.py**: Documentation generation validation
  - Sphinx build success
  - HTML output verification
  - Warning threshold checks

### Writing New Tests

When adding new features to the template, add corresponding tests:

```python
def test_new_feature(tmp_path: Path) -> None:
    """Test description."""
    # Arrange
    answers = {
        "project_name": "Test Project",
        "package_name": "test_pkg",
        # ... other required answers
        "new_option": "value",
    }
    
    # Act
    project_dir = render_template(tmp_path, answers)
    
    # Assert
    expected_file = project_dir / "expected_file.txt"
    assert expected_file.exists()
    content = expected_file.read_text()
    assert "expected_content" in content
```

## Code Style

### Python Code

Follow PEP 8 and use modern Python practices:

```powershell
# Run ruff for linting
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

**Style Guidelines:**
- Use type hints for function signatures
- Prefer f-strings over `.format()` or `%`
- Maximum line length: 120 characters
- Use descriptive variable names
- Add docstrings for public functions

### Jinja2 Templates

**Guidelines:**
- Use `{{ variable }}` for substitution
- Use `{% if condition %}` for conditionals
- Keep logic simple; complex logic belongs in hooks
- Add comments for non-obvious template logic
- Test with various input combinations

Example:
```jinja
# Good
name = "{{ package_name | replace('-', '_') }}"

# Avoid complex expressions
# Bad
name = "{{ package_name.replace('-', '_').upper()[:10] if condition else 'default' }}"
```

### Rust Code (in templates)

Follow Rust conventions:
- Use `rustfmt` for formatting
- Follow Rust naming conventions (snake_case for functions/variables)
- Use `clippy` for linting
- Add doc comments for public APIs

### YAML Configuration

- Use 2-space indentation
- Quote strings containing special characters
- Add comments for non-obvious configuration
- Keep structure aligned and readable

## Commit Guidelines

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or modifications
- `refactor`: Code refactoring
- `style`: Code style changes (formatting, etc.)
- `chore`: Build process or auxiliary tool changes
- `ci`: CI/CD changes

**Examples:**
```
feat(template): add support for Python 3.13

Add Python 3.13 to the list of supported versions in copier.yaml
and update PyO3 to 0.27 for compatibility.

Closes #42
```

```
fix(tests): handle Unicode errors in subprocess output

Add encoding parameter to subprocess.run calls to prevent
UnicodeDecodeError on Windows when reading compiler output.
```

```
docs(readme): update quick start instructions

- Add uv installation step
- Clarify Rust toolchain requirements
- Fix typo in build command
```

## Submitting Changes

### Pull Request Process

1. **Update your branch** with the latest upstream changes:
   ```powershell
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests** to ensure everything passes:
   ```powershell
   python -m pytest tests/integration/ -v
   ```

3. **Test the template** manually:
   ```powershell
   copier copy template ../test-pr-output --trust
   cd ../test-pr-output
   uv sync --group dev
   uv run maturin develop
   uv run pytest
   ```

4. **Push your branch** to your fork:
   ```powershell
   git push origin feature/add-new-option
   ```

5. **Create a Pull Request** on GitHub:
   - Use a clear, descriptive title
   - Reference related issues
   - Describe what changed and why
   - Include testing steps
   - Add screenshots for UI/docs changes

### Pull Request Template

```markdown
## Description
Brief description of changes

## Related Issues
Fixes #123

## Changes Made
- Added X feature
- Fixed Y bug
- Updated Z documentation

## Testing
- [ ] All integration tests pass
- [ ] Manual template generation tested
- [ ] Generated project builds successfully
- [ ] Documentation reviewed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Tests added/updated for changes
- [ ] Documentation updated
- [ ] Commit messages follow conventional commits
```

### Review Process

- Maintainers will review your PR
- Address feedback by pushing new commits
- Once approved, maintainers will merge
- Keep PRs focused and reasonably sized

## Release Process

### Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking changes to template API or generated structure
- **MINOR** (0.1.0): New features, backward compatible
- **PATCH** (0.0.1): Bug fixes, backward compatible

### Release Checklist

For maintainers preparing a release:

1. **Update version** in relevant files
2. **Update CHANGELOG.md** with release notes
3. **Run full test suite**:
   ```powershell
   python -m pytest tests/integration/ -v
   ```
4. **Test template generation** manually
5. **Tag the release**:
   ```powershell
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```
6. **Create GitHub release** with notes
7. **Announce** in discussions/community channels

## Documentation

### Updating Documentation

When making changes, update relevant documentation:

- **README.md**: User-facing features and quick start
- **CONTRIBUTING.md**: Development and contribution process
- **Template README**: Generated project documentation
- **BUILDING.md template**: Build instructions for generated projects
- **Spec files**: Feature specifications in `specs/`

### Documentation Style

- Use clear, concise language
- Include code examples
- Provide context for decisions
- Keep formatting consistent
- Test all command examples

## Questions or Problems?

- **Bug reports**: Open an issue with reproduction steps
- **Feature requests**: Open an issue with use case description
- **Questions**: Use GitHub Discussions
- **Security issues**: Email maintainers directly (see README)

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes for significant contributions
- Project documentation for major features

Thank you for contributing! 🎉
