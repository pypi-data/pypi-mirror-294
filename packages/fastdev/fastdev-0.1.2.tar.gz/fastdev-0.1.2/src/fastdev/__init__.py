import logging
import logging.config

from rich.logging import RichHandler

from fastdev.io import dump, load
from fastdev.utils.tui import console

logger = logging.getLogger("fastdev")
logger.setLevel("INFO")
logger.addHandler(RichHandler(console=console, show_path=False, log_time_format="[%X]"))

__all__ = ["load", "dump", "console"]
