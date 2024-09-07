import logging
import threading
import time
from openai import OpenAI, RateLimitError, AuthenticationError

from morix.helpers import clear_to_marker, set_marker
from .config_loader import config
from typing import List, Dict, Any

client = OpenAI()
logger = logging.getLogger(__name__)

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
        clear_to_marker()


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
        logger.info("Chat completion request successfully executed.")

    except RateLimitError as rle:
        logger.critical(f"Rate limit exceeded: {rle.message}")

    except AuthenticationError as ae:
        logger.critical("Authentication error. Check the API key.")

    except Exception as e:
        logger.critical(f"Error generating response from API: {e}")
        logger.debug("Stack trace:", exc_info=True)
    finally:
        spinner.stop()
        print()  # move to a new line after stopping the spinner

    return response
