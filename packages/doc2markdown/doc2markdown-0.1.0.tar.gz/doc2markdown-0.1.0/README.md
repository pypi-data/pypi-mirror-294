# 📄 doc2markdown

`doc2markdown` is a Python command-line tool that converts various document formats (PDF, PPTX, DOCX) to Markdown. It processes files in a given directory and its subdirectories, maintaining the original folder structure in the output.

## ✨ Features

- 📑 Converts PDF, PPTX, and DOCX files to Markdown format
- 🗂️ Preserves folder structure from input to output
- 💻 Command-line interface for easy use and integration with other tools
- 🔍 Verbose mode for detailed processing information

## ⚙️ Installation

To install `doc2markdown`, run the following command:

```bash
pip install doc2markdown
```

This will install `doc2markdown` along with its dependencies.

## 🚀 Usage

Basic usage:

```bash
doc2markdown /path/to/input/file.pdf /path/to/output/folder 
```

```bash
doc2markdown /path/to/input/folder /path/to/output/folder
```

With verbose output:

```bash
doc2markdown /path/to/input/folder /path/to/output/folder -v
```

For help and more options:

```bash
doc2markdown --help
```

## 🛠️ Requirements

- Python 3.6+
- PyPDF2
- python-pptx
- python-docx

These dependencies will be automatically installed when you install `doc2markdown` using pip.

## 🚀 Future Improvements

We're constantly working to improve doc2markdown. Here are some features and enhancements we're considering for future releases:

### TODO:

- [ ] Implement parallel processing for faster conversion of multiple files
- [ ] Add a progress bar for large batches of file conversions
- [ ] Create a plugin system for easy addition of new file format converters
- [ ] Implement comprehensive unit tests for each converter function
- [ ] Add logging mechanism for better debugging and user feedback
- [ ] Implement input sanitization for enhanced security
- [ ] Add type hints throughout the codebase for improved readability and maintainability
- [ ] Create a CONTRIBUTING.md file with guidelines for contributors

We welcome contributions from the community to help implement these features and improve doc2markdown. If you're interested in working on any of these tasks, please check our issues page or submit a pull request.

## 📝 Changelog

### [0.1.1] 
- Added File as well as folder support
- Improved the CLI messaging

### [0.1.0] 
- Initial release
- Basic functionality to convert PDF, PPTX, and DOCX files to Markdown
- Command-line interface with verbose mode option

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License.

## 🙏 Acknowledgements 

This tool was inspired by the need for easy conversion of various document formats to Markdown for use with Large Language Models and other text processing applications.

## Contributing

### Bumping the Version

To bump the version of the project, use the `bump_version.py` script:

1. Navigate to the project root directory.
2. Run the script with the following command:

   ```bash
   python bump_version.py doc2markdown/__init__.py [major|minor|patch]
   ```

   Replace `[major|minor|patch]` with the type of version bump you want to perform.

3. Commit the changes:

   ```bash
   git add doc2markdown/__init__.py
   git commit -m "Bump version to x.y.z"
   ```

4. Tag the new version:

   ```bash
   git tag -a vx.y.z -m "Version x.y.z"
   ```

5. Push the changes and tags:

   ```bash
   git push origin main
   git push --tags
   ```

This process will update the version number in the `__init__.py` file and create a new git tag for the release.
