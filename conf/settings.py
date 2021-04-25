"""
                Copyright (C) 2020 Theodoros Siklafidis

    This file is part of GRATIS.

    GRATIS is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GRATIS is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GRATIS. If not, see <https://www.gnu.org/licenses/>.
"""

import json
from enum import Enum

from conf.general import SETTINGS_PATH


class Themes(Enum):
    LIGHT = 'light'
    DARK = 'dark'


def load_settings():
    with open(SETTINGS_PATH) as f:
        try:
            SETTINGS = json.load(f)
            return SETTINGS
        except Exception:
            exit(1)


def get_theme() -> str:
    return load_settings()['theme']


def commit_settings(settings: dict):
    with open(SETTINGS_PATH, 'w') as _:
        json.dump(settings, _, indent=2)
