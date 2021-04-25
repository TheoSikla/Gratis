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

import os

from conf.styles import *
from conf.strings import *
from conf.general import BASE_DIR

APP_NAME = 'Gratis'

# Directories
OUTPUT_FILES_DIRECTORY_NAME = 'output_files'
OUTPUT_FILES_DIRECTORY = os.path.join(BASE_DIR, OUTPUT_FILES_DIRECTORY_NAME)

# Images
IMAGES_FOLDER = os.path.join(BASE_DIR, 'images')
BROWSE_IMAGE_FILENAME = 'folder.png'
DELETE_IMAGE_FILENAME = 'delete.png'
DOWN_IMAGE_FILENAME = 'down.png'
UP_IMAGE_FILENAME = 'up.png'
LIGHT_THEME_IMAGE_FILENAME = 'light_theme.png'
DARK_THEME_IMAGE_FILENAME = 'dark_theme.png'
BROWSE_IMAGE_PATH = os.path.join(IMAGES_FOLDER, BROWSE_IMAGE_FILENAME)
DELETE_IMAGE_PATH = os.path.join(IMAGES_FOLDER, DELETE_IMAGE_FILENAME)
DOWN_IMAGE_PATH = os.path.join(IMAGES_FOLDER, DOWN_IMAGE_FILENAME)
UP_IMAGE_PATH = os.path.join(IMAGES_FOLDER, UP_IMAGE_FILENAME)
LIGHT_THEME_IMAGE_PATH = os.path.join(IMAGES_FOLDER, LIGHT_THEME_IMAGE_FILENAME)
DARK_THEME_IMAGE_PATH = os.path.join(IMAGES_FOLDER, DARK_THEME_IMAGE_FILENAME)


