
# FileContentExtractor

**Languages:** [English](README.md) | [한국어](README_ko.md)

`FileContentExtractor` is a Python package designed to recursively extract and save the contents of text files in a directory. It provides options to ignore specific files or directories and outputs file paths as either absolute or relative paths.

## Features

- Recursively traverses directories and extracts the content of text files.
- Allows you to ignore specific files, directories, or patterns using a `.ignorelist` file.
- Outputs file paths as either relative or absolute paths.
- Skips non-text files (like binary files).

## Installation

You can install the package via `pip`:

```bash
pip install file-content-extractor
```

## Usage

1. **Run the command**:

   - Default usage (relative paths):

     ```bash
     file_extractor
     ```

   - Use absolute paths:

     ```bash
     file_extractor --absolute
     ```

2. **Ignore list**:

   Create a `.ignorelist` file to specify files, directories, or patterns to ignore:

   - `*.log` - Ignore all files ending with `.log`
   - `__pycache__` - Ignore the `__pycache__` directory
   - `src/data/*` - Ignore all files in the `src/data/` directory

## Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

- **Daniel** - [joonheeu](https://github.com/joonheeu) - daniel@udit.one
- **Company**: UDIT