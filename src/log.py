from __future__ import annotations

import logging
from typing import Final

L: Final = logging.getLogger(__name__)


def configure_basic_logging() -> None:
    """
    Log config
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s:%(module)s - %(funcName)s:%(lineno)s] %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
    )
