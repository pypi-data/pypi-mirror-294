import argparse
import os
import shutil
import time
import logging
from distutils.core import setup
from Cython.Build import cythonize
import concurrent.futures

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

ROOT_PATH = os.path.abspath("")
PROJECT_NAME = ROOT_PATH.split("/")[-1]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--ignore", default=["venv", ".venv"], nargs="+", help="ignore files for compile."
    )
    parser.add_argument("-d", "--dir", default="dist", help="result directory.")
    parser.add_argument("-v", "--version", default=3, help="python version.")
    parser.add_argument("-c", "--copy_py", default=[], nargs="+", help="copy py files.")
    parser.add_argument(
        "-p", "--parallel", type=int, default=os.cpu_count(), help="number of parallel workers (default: number of CPU cores)."
    )
    return parser.parse_args()


def ls(dir=""):
    """Return all relative path under the current folder."""
    dir_path = os.path.join(ROOT_PATH, dir)
    for filename in os.listdir(dir_path):
        absolute_file_path = os.path.join(dir_path, filename)
        file_path = os.path.join(dir, filename)
        if filename.startswith("."):
            continue
        if os.path.isdir(absolute_file_path) and not filename.startswith("__"):
            for file in ls(file_path):
                yield file
        else:
            yield file_path


def is_migration_file(file):
    """Check if the file is a Django migration file."""
    return "migrations" in file.replace("\\", "/").split("/")


def copy_ignore(args):
    """Copy ignore files"""
    files = ls()
    for file in files:
        file_arr = file.split("/")
        if file_arr[0] == args.dir:
            continue
        suffix = os.path.splitext(file)[1]
        if not suffix:
            continue
        if file_arr[0] not in args.copy_py and file not in args.copy_py:
            if suffix in (".pyc", ".pyx"):
                continue
            elif suffix == ".py":
                continue
        src = os.path.join(ROOT_PATH, file)
        dst = os.path.join(
            ROOT_PATH, os.path.join(args.dir, file.replace(ROOT_PATH, "", 1))
        )
        dir = "/".join(dst.split("/")[:-1])
        if not os.path.exists(dir):
            os.makedirs(dir)
        shutil.copyfile(src, dst)
        logger.debug(f"Copied {src} to {dst}")


def compile_module(module, args, dist_temp):
    """Compile a single module."""
    try:
        setup(
            ext_modules=cythonize(
                module, compiler_directives={"language_level": args.version}
            ),
            script_args=[
                "build_ext",
                "-b",
                os.path.join("", args.dir),
                "-t",
                dist_temp,
            ],
        )
    except Exception as e:
        logger.error(f"Error during setup: {e}")


def build(args):
    """py -> c -> so"""
    start = time.time()
    logger.info("Build started")
    files = list(ls())
    module_list = list()
    for file in files:
        suffix = os.path.splitext(file)[1]
        if not suffix:
            continue
        elif file.split("/")[0] in args.ignore or file in args.ignore:
            continue
        elif is_migration_file(file):
            logger.debug(f"Skipped migration file {file}")
            continue
        elif suffix in (".pyc", ".pyx"):
            continue
        elif suffix == ".py":
            module_list.append(file)
            logger.debug(f"Added {file} to module list")

    dist_temp = os.path.join(os.path.join("", args.dir), "temp")

    with concurrent.futures.ProcessPoolExecutor(max_workers=args.parallel) as executor:
        futures = [
            executor.submit(compile_module, module, args, dist_temp)
            for module in module_list
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error during compilation: {e}")

    if os.path.exists(dist_temp):
        shutil.rmtree(dist_temp)
    for file in ls():
        if not file.endswith(".c"):
            continue
        os.remove(os.path.join(ROOT_PATH, file))
        logger.debug(f"Removed {file}")

    copy_ignore(args)
    end = time.time()
    logger.info(f"Build complete in {end - start:.2f} seconds")


def main():
    args = parse_args()
    logger.info("Starting main function")
    build(args)


if __name__ == "__main__":
    main()
