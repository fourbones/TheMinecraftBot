"""Utility helpers for reading and writing persistent user data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "user_data.json"


def load_user_data() -> Dict[str, Any]:
    """Return the persisted user data as a dictionary.

    The data file is created automatically the first time this function is
    called so that other modules can rely on its existence.
    """

    if not DATA_PATH.exists():
        save_user_data({})
        return {}

    with DATA_PATH.open("r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # If the file somehow becomes corrupted we start with a clean slate
            # to avoid crashing the bot and blocking whitelist updates.
            save_user_data({})
            return {}


def save_user_data(data: Dict[str, Any]) -> None:
    """Persist the provided user data to disk."""

    with DATA_PATH.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

