"""File sorter"""
import os
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor


def process_file(file_path: str, target_dir: str) -> None:
    extension = os.path.splitext(file_path)[1].lstrip('.').lower()
    extension_dir = os.path.join(target_dir, extension)
    os.makedirs(extension_dir, exist_ok=True)

    target_path = os.path.join(extension_dir, os.path.basename(file_path))
    shutil.copy2(file_path, target_path)

def process_directory(source_dir):
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            yield file_path

def sort_files(source_dir: str, target_dir: str) -> None:
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with ThreadPoolExecutor() as executor:
        for file_path in process_directory(source_dir):
            executor.submit(process_file, file_path, target_dir)

def main() -> None:
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
