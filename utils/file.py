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

import re
from os import listdir
from os.path import isfile, join

file_format_regex = '^[0-9]{2}-[0-9]{2}-[0-9]{4}_[0-9]{2}:[0-9]{2}:[0-9]{2}'
file_format_regex_compiled = re.compile(file_format_regex)


def locate_latest_file(directory: str, graph_file_type: str):
    """
    Locate latest file inside a given directory using a date format of '%d-%m-%Y_%H:%M:%S'
    """
    return [
        f for f in listdir(directory) if (
                isfile(join(directory, f)) and
                file_format_regex_compiled.search(f) and
                graph_file_type in f.lower()
        )
    ][-1]
