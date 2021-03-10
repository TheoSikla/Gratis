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

from enum import Enum


class MessageType(Enum):
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'
    SUCCESS = 'success'


class MessagePrefix(Enum):
    ERROR = '[-]'
    WARNING = '[!]'
    INFO = '[*]'
    SUCCESS = '[+]'


class MessageColor(Enum):
    ERROR = '\u001b[38;5;197m'
    WARNING = '\u001b[38;5;220m'
    INFO = '\u001b[38;5;81m'
    SUCCESS = '\u001b[38;5;48m'
    END = '\u001b[0m'


AVAILABLE_MESSAGE_PREFIXES = {k.value: v.value for k, v in zip(MessageType, MessagePrefix)}
AVAILABLE_MESSAGE_PREFIX_COLOURS = {k.value: v.value for k, v in zip(MessageType, MessageColor)}
