# Agent Instructions for cp-cache

This is a Python CLI tool for copying SPlayer cache files and concatenating audio tracks using ffmpeg.

## Build Commands

### Setup
```bash
# Install dependencies (uses uv)
uv sync

# Activate virtual environment
source .venv/bin/activate
```

### Running
```bash
# Run the CLI directly
uv run cp-cache

# Or after activating venv
python -m cp_cache
```

### Building
```bash
# Build wheel (uses hatchling)
uv build

# Install in editable mode
uv pip install -e .
```

### Testing
```bash
# Run all tests (when tests exist)
uv run pytest

# Run a single test file
uv run pytest tests/test_specific.py

# Run a single test function
uv run pytest tests/test_specific.py::test_function_name

# Run with coverage
uv run pytest --cov=cp_cache --cov-report=term-missing
```

### Linting and Formatting
```bash
# Format code with ruff
uv run ruff format .

# Check linting
uv run ruff check .

# Fix auto-fixable lint issues
uv run ruff check . --fix

# Type checking with mypy
uv run mypy src/cp_cache
```

## Code Style Guidelines

### Python Version
- **Python 3.13+** (defined in `.python-version` and `pyproject.toml`)
- Use modern Python features (pathlib, type hints, walrus operator where appropriate)

### Imports
- Group imports: stdlib first, third-party second, local third
- Use absolute imports
- Sort imports with ruff/isort
- Prefer `pathlib.Path` over `os.path`

Example:
```python
import pathlib
import os
import shutil

import ffmpeg
```

### Type Hints
- Use type hints for function parameters and return values
- Use `pathlib.Path` type for file paths
- Use built-in generics (e.g., `list[pathlib.Path]` instead of `List[Path]`)

Example:
```python
def concat_tracks(tracklist: list[pathlib.Path], output_file: pathlib.Path) -> bool:
    ...
```

### Naming Conventions
- Functions: `snake_case`
- Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Modules: `snake_case`
- Private functions: `_leading_underscore`

### Error Handling
- Use try/except for expected errors (user input, file operations)
- Print user-friendly error messages
- Return boolean or exit codes from CLI functions
- Handle `KeyboardInterrupt` and `EOFError` for interactive input

Example:
```python
try:
    track_id = int(input("Enter track ID: ").strip())
except ValueError:
    print("Invalid track ID")
    continue
except (KeyboardInterrupt, EOFError):
    break
```

### String Formatting
- Use f-strings for string formatting
- Use `.resolve()` and `.stem` for path operations

Example:
```python
output_file = target_path / f"{album_name}.mp3"
metadata = f"title={output_file.stem}"
```

### Comments
- Use English for comments
- Chinese comments are acceptable in this codebase (existing convention)
- Keep comments concise and meaningful
- Use inline comments sparingly

### File Operations
- Use `pathlib.Path` for all path operations
- Use `.expanduser()` for paths with `~`
- Use `.resolve()` to get absolute paths
- Use `shutil.move()` for file operations
- Use `os.makedirs(..., exist_ok=True)` for directory creation

### CLI Design
- Use `input()` for interactive prompts
- Provide default options (Y/n prompts)
- Validate user input immediately
- Show confirmation of selected options
- Support `^C` (KeyboardInterrupt) and `^D` (EOFError) for graceful exit

### Dependencies
- Add dependencies to `pyproject.toml` under `[project]dependencies`
- Uses `ffmpeg-python` for audio processing
- Minimum versions specified with `>=`

### Project Structure
```
src/
  cp_cache/
    __init__.py    # Main module with CLI entry point
```

### Git
- Commit message style: concise, lowercase (based on existing commit)
- Do not commit: `__pycache__/`, `.venv/`, build artifacts

## Dependencies Management

This project uses `uv` for fast Python package management:
- `uv sync` - Sync dependencies from lock file
- `uv add <package>` - Add a new dependency
- `uv lock` - Update lock file
- `uv run` - Run commands in the virtual environment

## Notes

- This tool interacts with SPlayer's cache directory (`~/.config/SPlayer/DataCache/music`)
- Requires ffmpeg installed on the system
- Supports mp3, wav, flac audio formats (though outputs as mp3)
