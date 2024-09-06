# Neverland Tools

A collection of tools for development.

## Installation

```bash
pip install neverland-tools
```

## neverland-compile Usage

`neverland-compile` is a tool designed to compile Python files into C extensions using Cython. This can help improve the performance of your Python code. Below is a detailed guide on how to use `neverland-compile`.

### Command-Line Arguments

- `-i, --ignore`: List of files or directories to ignore during compilation.
- `-d, --dir`: The directory where the compiled files will be stored. Default is `dist`.
- `-v, --version`: The Python language level to use for the compilation. Default is `3`.
- `-c, --copy_py`: List of Python files to copy without compiling.
- `-p, --parallel`: Number of parallel workers to use for compilation. Default is the number of CPU cores.

### Example Usage

#### Basic Compilation

To compile all Python files in the current directory and store the compiled files in the `dist` directory:

```bash
neverland-compile
```

#### Ignoring Specific Files

To ignore specific files or directories during compilation:

```bash
neverland-compile -i file_to_ignore.py dir_to_ignore