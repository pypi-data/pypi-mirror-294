import argparse
import logging
import os
from .helpers import check_git_presence
from .conversation import conversation
from .config_loader import open_config_file, config
from .version import PROGRAM_NAME, PROGRAM_VERSION
import sys

# Добавляем корневую директорию в PYTHONPATH, если она не там
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logging.basicConfig(level=config.log_level, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description="Scanning the folder and sending to GPT")
    parser.add_argument('path', nargs='?', default=os.getcwd(), help="Path to the directory to scan")
    parser.add_argument("-c", "--contents", action="store_true", help="Scan directory structure and files content")
    parser.add_argument("-s", "--structure-only", action="store_true", help="Scan directory structure")
    parser.add_argument("--config", action="store_true", help="Open configuration file")
    parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {PROGRAM_VERSION}")
    parser.add_argument('-m', '--message', help="Message to send as initial user input")
    return parser.parse_args()


def handle_command(args: argparse.Namespace):
    if args.config:
        open_config_file()
    else:
        work_folder = args.path

        if not os.path.isdir(work_folder):
            logger.error(f"Error: Path '{work_folder}' is not a directory.")
            raise SystemExit(1)

        check_git_presence(work_folder)

        need_scan, structure_only = False, False
        if args.structure_only:
            need_scan, structure_only = True, True
        elif args.contents:
            need_scan = True

        logger.info(f"Starting work on the project at: {os.path.abspath(work_folder)}")
        conversation(work_folder, need_scan, structure_only, args.message)


def main() -> None:
    args = parse_args()

    logger.info(f"Using configs in: {config.path}")
    handle_command(args)

if __name__ == '__main__':
    main()
