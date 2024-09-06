# Neverland Tools

A collection of tools for development.

## Installation

```bash
pip install neverland-tools
```

## neverland-compile 


### Overview

`neverland-compile` is a tool designed to compile Python files into C extensions using Cython. This can help improve the performance of your Python code. The script supports parallel compilation to speed up the process, and it allows you to ignore certain files or directories, copy specific Python files without compiling them, and specify the output directory and Python language version.

### Command-Line Arguments

1. **`-i, --ignore`**: List of files or directories to ignore during compilation.
   - **Type**: List of strings
   - **Default**: `[]` (empty list)
   - **Example**: `-i file_to_ignore.py dir_to_ignore`

2. **`-d, --dir`**: The directory where the compiled files will be stored.
   - **Type**: String
   - **Default**: `dist`
   - **Example**: `-d output_directory`

3. **`-v, --version`**: The Python language level to use for the compilation.
   - **Type**: Integer
   - **Default**: `3`
   - **Example**: `-v 2` for Python 2.x compatibility

4. **`-c, --copy_py`**: List of Python files to copy without compiling.
   - **Type**: List of strings
   - **Default**: `[]` (empty list)
   - **Example**: `-c script1.py script2.py`

5. **`-p, --parallel`**: Number of parallel workers to use for compilation.
   - **Type**: Integer
   - **Default**: Number of CPU cores available
   - **Example**: `-p 4` to use 4 parallel workers

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
```

#### Specifying Output Directory

To specify a custom output directory for the compiled files:

```bash
neverland-compile -d output_directory
```

#### Specifying Python Version

To specify the Python language level for the compilation:

```bash
neverland-compile -v 2
```

#### Copying Specific Python Files Without Compiling

To copy specific Python files without compiling them:

```bash
neverland-compile -c script1.py script2.py
```

#### Using Parallel Compilation

To use a specific number of parallel workers:

```bash
neverland-compile -p 4
```

### Script Breakdown

1. **Argument Parsing**: The `parse_args` function uses `argparse` to handle command-line arguments.
2. **File Listing**: The `ls` function recursively lists all files in the directory.
3. **Migration File Check**: The `is_migration_file` function checks if a file is a Django migration file.
4. **Copying Ignored Files**: The `copy_ignore` function copies files that should be ignored during compilation.
5. **Compilation**: The `compile_module` function compiles a single module using Cython.
6. **Build Process**: The `build` function handles the overall build process, including parallel compilation and cleanup.
7. **Main Function**: The `main` function is the entry point of the script, which parses arguments and calls the build function.

### Conclusion

`neverland-compile` is a versatile tool for compiling Python files into C extensions. By using the provided command-line arguments, you can customize the compilation process to suit your needs, whether it's ignoring specific files, copying certain Python files, or leveraging parallel processing to speed up the compilation.