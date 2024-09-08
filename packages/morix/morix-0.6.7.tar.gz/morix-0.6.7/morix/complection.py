import logging
import os
import sys
import threading
import time
from openai import OpenAI, OpenAIError, RateLimitError, AuthenticationError

from morix.helpers import clear_to_marker, set_marker
from .config_loader import config
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set.")
        sys.exit(1)
    client = OpenAI()
except OpenAIError as e:
    logger.Logger.critical(f"Error initializing OpenAI client: {e}")
    sys.exit(1)

class DotSpinner:
    def __init__(self):
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run)

    def _run(self):
        set_marker()
        dot_count = 0
        while not self.stop_event.is_set():
            print('.', end='', flush=True)
            dot_count += 1
            if dot_count >= 15:
                print('\r', end='', flush=True)  # return carriage for overwriting the dot line
                dot_count = 0
            time.sleep(1)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()


def chat_completion_request(messages: List[Dict[str, Any]], functions=None) -> Dict:
    """Sends a request to OpenAI."""

    spinner = DotSpinner()
    spinner.start()
    response = None

    try:
        response = client.chat.completions.create(
            model=config.gpt_model,
            messages=messages,
            tools=functions,
            parallel_tool_calls=True,
        )

    except RateLimitError as rle:
        logger.critical(f"Rate limit exceeded: {rle.message}")

    except AuthenticationError as ae:
        logger.critical("Authentication error. Check the API key.")
        exit(1)

    except Exception as e:
        logger.critical(f"Error generating response from API: {e}")
        logger.debug("Stack trace:", exc_info=True)
        exit(1)

    finally:
        spinner.stop()
        print()

    clear_to_marker()
    logger.info("Chat completion request successfully executed.")
    return response
