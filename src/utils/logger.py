"""
Configures logging once, in one place, instead of every module calling
logging.basicConfig() independently.
"""

import logging


def setup_logging(memory_filepath):
    """
    memory_filepath is the path to data/memory.json -- the error log lives
    alongside it, in data/system_errors.log.
    """
    memory_filepath.parent.mkdir(parents=True, exist_ok=True)
    log_file = memory_filepath.parent / "system_errors.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
