# CodeUpdater

[🇺🇸English](README.md) | [🇰🇷한국어](README_ko.md)

**CodeUpdater** is a Python-based tool designed to automate the process of updating, inserting, or deleting lines in multiple files within a project directory based on a specified JSON configuration.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [JSON Configuration](#json-configuration)
- [Example](#example)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Update**: Replace specific lines in a file with new content.
- **Insert**: Insert new lines at a specific position in a file, pushing existing lines downward.
- **Delete**: Remove specific lines from a file.

## Installation

To install CodeUpdater, you can use `pip`. Run the following command:

```bash
pip install code-updater
```

Or, if you are developing or want to install it from a local copy:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/joonheeu/code-updater.git
   cd code-updater
   ```

2. Install the package locally:

   ```bash
   pip install .
   ```

## Usage

To use `CodeUpdater`, ensure that you have Python installed. Then, create an `updates.json` file in the root directory of your project, and structure it according to the configuration described below.

You can run the script using the following command:

```bash
cup [OPTIONS] {project_root_path}
```

Replace `{project_root_path}` with the root directory of your project where the files are located.

### Options

- `-h`, `--help`: Show the help message and exit.
- `-V`, `--version`: Show the current version of `CodeUpdater` and exit.

## JSON Configuration

The JSON file should describe the operations you want to perform. Below is the structure of the JSON file:

```json
[
  {
    "path": "src/example.py",
    "line": 42,
    "type": "update",  # Type of operation: "update", "insert", or "delete"
    "replace": [
      "new line 42 content",
      "new line 43 content"
    ]
  }
]
```

### Type

- **update**: Replaces the lines starting from the specified line number with the provided content in the "replace" list.
- **insert**: Inserts the lines from the "replace" list starting at the specified line number, shifting existing lines downward.
- **delete**: Removes the line specified by the line number. The "replace" field is not needed for this operation.

### Example

Here’s an example configuration:

```json
[
  {
    "path": "src/example.py",
    "line": 42,
    "type": "update",
    "replace": [
      "updated line 42 content",
      "updated line 43 content"
    ]
  },
  {
    "path": "src/example.py",
    "line": 10,
    "type": "insert",
    "replace": [
      "inserted line 10 content",
      "inserted line 11 content"
    ]
  },
  {
    "path": "src/example.py",
    "line": 15,
    "type": "delete"
  }
]
```

In this example:
- The lines at 42 and 43 in `src/example.py` will be updated.
- New lines will be inserted at line 10, and existing lines will be shifted downward.
- The line at 15 will be deleted.

## Logging

The tool generates logs in the `logs/` directory inside the specified project root. Each log file is timestamped and details the changes made to the files. The log includes both the original and the updated content for comparison.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. If you find any issues or have suggestions, feel free to open an issue on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

**Author:** Daniel  
**Email:** [daniel@udit.one](mailto:daniel@udit.one)  
**Company:** UDIT

For more details, visit the GitHub repository: [CodeUpdater](https://github.com/joonheeu/code-updater)
