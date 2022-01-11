# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import sys
from pathlib import Path
from typing import Final

from dynaconf import Dynaconf

_THIS_DIR: Final[Path] = Path(__file__).resolve(strict=True).parent

settings: Final = Dynaconf(
    core_loaders=("TOML",),
    envvar_prefix=False,
    environments=True,
    load_dotenv=not ("pytest" in sys.modules),
    dotenv_verbose=True,
    settings_files=[_THIS_DIR / ".." / "settings.toml"],
)

__all__ = ("settings",)
