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
import platform

try:
    re.search(r'\bWindows\b', platform.platform()).group()
    platform_type = "Windows"
    transform = "1000x600"
    path_escape = "/"
except AttributeError:
    try:
        re.search(r'\bLinux\b', platform.platform()).group()
        platform_type = "Linux"
        transform = "1100x600"
        path_escape = "/"
    except AttributeError:
        try:
            re.search(r'\bDarwin\b', platform.platform()).group()
            platform_type = "OSX"
            transform = "1000x600"
            path_escape = "/"
        except AttributeError:
            platform_type = "Unknown"
            transform = "1000x600"
            path_escape = "/"
