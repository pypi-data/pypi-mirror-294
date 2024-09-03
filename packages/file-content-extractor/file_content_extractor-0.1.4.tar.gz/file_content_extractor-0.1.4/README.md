# FileContentExtractor

**Languages:** [🇺🇸English](README.md) | [🇰🇷한국어](README_ko.md)

`FileContentExtractor` is a versatile Python tool designed to recursively extract and save the contents of text files in a directory. It provides various options to ignore specific files or directories, filter files based on several criteria, and output file paths as either absolute or relative paths. The tool also includes user confirmation, version display, and help options for better usability.

## Features

- Recursively traverses directories and extracts the content of text files.
- Allows you to ignore specific files, directories, or patterns using a `.ignorelist` file.
- Outputs file paths as either relative or absolute paths.
- Supports filtering files by extension, size, and modification date.
- Allows splitting output into multiple files based on size.
- Displays a progress bar during extraction.
- Prompts user confirmation before proceeding with extraction.
- Provides version information and help details via command-line options.

## Installation

You can install the package via `pip`:

```bash
pip install file-content-extractor
```

## Usage

1. **Basic command**:

   - Default usage (relative paths):

     ```bash
     file_extractor
     ```

     - After running this command, you will be prompted to confirm the extraction by typing `y`.

   - Use absolute paths:

     ```bash
     file_extractor -a
     ```

2. **Specify additional options**:

   - Ignore specific files or directories:

     ```bash
     file_extractor -i my_ignore_list.txt
     ```

   - Save output to a custom file:

     ```bash
     file_extractor -o my_output.txt
     ```

   - Filter by file extension, size, and modification date:

     ```bash
     file_extractor -e .txt,.py -m 1024 -M 1048576 -d 2023-01-01
     ```

   - Split output into multiple files:

     ```bash
     file_extractor -s 10485760
     ```

   - Specify the directory to start extraction from:

     ```bash
     file_extractor -p /path/to/directory
     ```

3. **Check version**:

   - To display the current version of the tool:

     ```bash
     file_extractor -v
     ```

4. **Help**:

   - To display help information and usage details:

     ```bash
     file_extractor -h
     ```

## Options

- `-a`, `--absolute`: Use absolute paths in the output.
- `-i <file>`, `--ignore=<file>`: Specify a custom ignore file (default is `.ignorelist`).
- `-o <file>`, `--output=<file>`: Specify a custom output file (default is `output.txt`).
- `-e <ext1,ext2,...>`, `--extensions=<ext1,ext2,...>`: Specify file extensions to include (e.g., `.txt,.py`).
- `-m <bytes>`, `--min-size=<bytes>`: Specify minimum file size to include.
- `-M <bytes>`, `--max-size=<bytes>`: Specify maximum file size to include.
- `-d <YYYY-MM-DD>`, `--modified-after=<YYYY-MM-DD>`: Include only files modified after a specific date.
- `-s <bytes>`, `--split-size=<bytes>`: Split output files into chunks of the specified size.
- `-p <directory>`, `--path=<directory>`: Specify the directory to start extraction from.
- `-h`, `--help`: Show this help message and exit.
- `-v`, `--version`: Show version information and exit.

## Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

- **Daniel** - [joonheeu](https://github.com/joonheeu) - daniel@udit.one
- **Company**: UDIT