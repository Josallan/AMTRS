import time
import logging
from retrying import retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('amtrs')

# Exponential backoff helper
def wait_exponential(attempt):
    # attempt is 1-based
    return min(10000, (2 ** attempt) * 100)

def backoff_on_exception(f):
    # wrapper to apply retry with exponential backoff
    return retry(wait_exponential_multiplier=100, stop_max_attempt_number=5)(f)
