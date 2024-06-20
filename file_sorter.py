"""File sorter, task 1"""
import os
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor


def process_file(file_path: str, target_dir: str) -> None:
    """This function takes a file path and a target directory as input
    parameters and moves the file to the appropriate subdirectory within
    the target directory based on its file extension. If the target
    subdirectory does not exist, it is created using `os.makedirs()`.
    The function uses `shutil.copy2()` to move the file instead of directly
    moving or renaming it, which ensures that file metadata and timestamps
    are preserved.

    Args:
        file_path (str): The path to the source file.
        target_dir (str): The path to the target directory.
    """
    extension = os.path.splitext(file_path)[1].lstrip('.').lower()
    extension_dir = os.path.join(target_dir, extension)
    os.makedirs(extension_dir, exist_ok=True)

    target_path = os.path.join(extension_dir, os.path.basename(file_path))
    shutil.copy2(file_path, target_path)

def process_directory(source_dir: str):
    """This generator function takes a source directory as input and iterates
    through all files in the source directory and its subdirectories. It yields
    the file paths for each file it encounters.

    Args:
        source_dir (str): The path to the source directory.

    Yields:
        str: The path to each file.
    """
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            yield file_path

def sort_files(source_dir: str, target_dir: str) -> None:
    """This function takes a source directory and a target directory as input
    parameters and uses multithreading with `ThreadPoolExecutor()` to process
    files in parallel using the `process_file()` function. It creates the
    target directory if it doesn't exist, and then calls the
    `process_directory()` generator function to get file paths. For each
    file path, a new thread is created, which processes the file by moving
    it to the appropriate subdirectory within the target directory based on
    its file extension using `os.makedirs()` and `shutil.copy2()`.


    Args:
        source_dir (str): The path to the source directory.
        target_dir (str): The path to the target directory.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with ThreadPoolExecutor() as executor:
        for file_path in process_directory(source_dir):
            executor.submit(process_file, file_path, target_dir)

def main() -> None:
    """This function serves as the entry point for the program. It checks
    the number of command-line arguments and prints usage instructions if
    the count is incorrect. If the correct number of arguments is provided,
    it sets the source directory to the first argument and the target directory
    to the second argument (or "dist" if no second argument is provided).
    It then checks if the source directory exists, and if so, calls the
    `sort_files()` function to process the files. Finally, it prints a message
    confirming that the files have been copied into the target directory.
    """
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 task-1.py source_directory target_directory")
        return

    source_directory = sys.argv[1]
    target_directory = sys.argv[2] if len(sys.argv) == 3 else "dist"

    if not os.path.exists(source_directory):
        print('No such directory.')
        return
    sort_files(source_directory, target_directory)
    print(f"Files copied into '{target_directory}'.")

if __name__ == "__main__":
    main()
