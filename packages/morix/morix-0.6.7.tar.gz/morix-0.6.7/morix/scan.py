import os
import fnmatch
import logging
from pathlib import Path
from .config_loader import load_config, is_development_mode, CONFIG_LOCAL_DIR, CONFIF_IGNORE_FILE
from .helpers import read_file_content
from typing import List

logger = logging.getLogger(__name__)

config = load_config()
text_extensions = set(config['text_extensions'])

def get_ignore_patterns_paths(scan_folder: str) -> List[str]:
    """Returns the paths to the ignore pattern files."""
    ignore_pattern_files = config['ignore_pattern_files']
    ignore_files_paths = []

    for file in ignore_pattern_files:
        expanded_path = os.path.expanduser(file)
        root_path = os.path.join(scan_folder, file)

        if os.path.exists(root_path):
            ignore_files_paths.append(root_path)
        elif os.path.exists(expanded_path):
            ignore_files_paths.append(expanded_path)

    if is_development_mode():
        dev_ignore_path = os.path.join(os.path.dirname(__file__), CONFIG_LOCAL_DIR, CONFIF_IGNORE_FILE)
        ignore_files_paths.append(dev_ignore_path)

    return ignore_files_paths

def read_ignore_file(ignore_files_paths: List[str]) -> List[str]:
    """Reads ignore pattern files and returns a list of patterns."""
    ignore_patterns = []
    for path in ignore_files_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as file:
                    ignore_patterns.extend(file.read().splitlines())
            except IOError as e:
                logger.error(f"Failed to read file {path}: {e}", exc_info=True)
        else:
            logger.error(f"File {path} does not exist")

    return ignore_patterns

def should_ignore(path: str, patterns: List[str]) -> bool:
    """Determines if a file should be ignored based on given patterns."""
    # Convert the path to a Path object
    path_obj = Path(path)
    # Get the parent folder name or the current folder name if parent is empty
    check_obj = path_obj.parent.name or path_obj.name

    # Check for match of parent folder or full path against any pattern
    for pattern in patterns:
        if fnmatch.fnmatch(check_obj, pattern) or fnmatch.fnmatch(path_obj.name, pattern):
            return True

        # Additional check for directories
        if path_obj.is_relative_to(Path.cwd()):  # If path is relative and in current directory
            if any(fnmatch.fnmatch(check_obj, f"{pattern}*") for pattern in patterns):
                return True

    return False

def is_text_file(file_path: str) -> bool:
    """Checks if a file is a text file based on its extension and content."""
    _, ext = os.path.splitext(file_path)
    if ext in text_extensions:
        return True

    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
            if b'\0' in chunk:
                return False

            try:
                chunk.decode('utf-8', errors='ignore')
                return True
            except (UnicodeDecodeError, IOError) as e:
                logger.error(f"Error reading file {file_path}: {e}", exc_info=True)
                return False
    except IOError as e:
        logger.error(f"File cannot be opened: {file_path}: {e}", exc_info=True)
        return False

def get_text_files(root: str, ignore_patterns: List[str]) -> List[str]:
    """Returns a list of text files, excluding ignored ones."""
    text_files = []
    try:
        for dirpath, dirnames, filenames in os.walk(root):
            new_dirnames = [d for d in dirnames if not should_ignore(os.path.relpath(os.path.join(dirpath, d), root), ignore_patterns)]
            for dirname in list(dirnames):  # Clone the original dirnames and remove content from the copy
                if dirname not in new_dirnames:
                    dirnames.remove(dirname)
            for filename in filenames:
                relpath = os.path.relpath(os.path.join(dirpath, filename), root)
                full_path = os.path.join(root, relpath)
                if not should_ignore(relpath, ignore_patterns) and is_text_file(full_path):
                    text_files.append(relpath)
    except Exception as e:
        logger.error(f"Error during scanning: {e}", exc_info=True)
    return text_files

def scan(scan_folder: str) -> str:
    """Scans a folder and returns the contents of all text files."""
    ignore_files_paths = get_ignore_patterns_paths(scan_folder)
    logger.debug(f"Files to search for ignore patterns: {ignore_files_paths}")
    ignore_patterns = read_ignore_file(ignore_files_paths)
    logger.debug(f"Ignore patterns: {ignore_patterns}")

    text_files = get_text_files(scan_folder, ignore_patterns)
    logger.debug(f"Files to scan: {text_files}")

    scan_result = "\n".join(
        f"{file}\n```\n{read_file_content(os.path.join(scan_folder, file))}\n```"
        for file in text_files
    )

    return scan_result

def get_project_structure(scan_folder: str) -> str:
    """Returns the project structure."""
    ignore_files_paths = get_ignore_patterns_paths(scan_folder)
    logger.debug(f"Files to search for ignore patterns: {ignore_files_paths}")
    ignore_patterns = read_ignore_file(ignore_files_paths)
    logger.debug(f"Ignore patterns: {ignore_patterns}")

    project_structure = []

    try:
        for dirpath, dirnames, filenames in os.walk(scan_folder):
            new_dirnames = [d for d in dirnames if not should_ignore(os.path.relpath(os.path.join(dirpath, d), scan_folder), ignore_patterns)]

            for dirname in list(dirnames):  # Clone the original dirnames and remove content from the copy
                if dirname not in new_dirnames:
                    dirnames.remove(dirname)

            for filename in filenames:
                relpath = os.path.relpath(os.path.join(dirpath, filename), scan_folder)
                if not should_ignore(relpath, ignore_patterns):
                    project_structure.append(relpath)

    except Exception as e:
        logger.error(f"Error scanning structure: {e}", exc_info=True)

    return "\n".join(project_structure)
