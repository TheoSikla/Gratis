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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_NAME = 'Gratis'

STYLES = {
    'default': {
        'main_frame_bg': 'azure3',
        'button': {
            'font': {
                'family': 'Dialog',
                'size': 9,
                'style': 'bold italic'
            },
            'bg': 'seashell3',
            'fg': 'black',
            'relief': 'flat',
            'width': 15
        },
        'frame': {
            'bg': 'azure3'
        },
        'radiobutton': {
            'font': {
                'family': 'Dialog',
                'size': 9,
                'style': 'bold italic'
            },
            'bg': 'azure3',
            'fg': 'black',
            'relief': 'flat',
        },
        'checkbutton': {
            'font': {
                'family': 'Dialog',
                'size': 9,
                'style': 'bold italic'
            },
            'bg': 'azure3',
            'fg': 'black',
            'relief': 'flat',
        }
    }
}

# Define Style
ACTIVE_STYLE = 'default'
STYLE = STYLES[ACTIVE_STYLE]

# Main Frame
MAIN_FRAME_BACKGROUND = STYLE['main_frame_bg']
MAIN_FRAME_PADX = 20
MAIN_FRAME_PADY = 20

# Button
BUTTON_FONT = (
    STYLE['button']['font']['family'], STYLE['button']['font']['size'], STYLE['button']['font']['style']
)
BUTTON_BACKGROUND = STYLE['button']['bg']
BUTTON_FOREGROUND = STYLE['button']['fg']
BUTTON_RELIEF = STYLE['button']['relief']
BUTTON_WIDTH = STYLE['button']['width']

# Frame
FRAME_BACKGROUND = STYLE['frame']['bg']

# Radiobutton
RADIOBUTTON_FONT = (
    STYLE['radiobutton']['font']['family'], STYLE['radiobutton']['font']['size'], STYLE['radiobutton']['font']['style']
)
RADIOBUTTON_BACKGROUND = STYLE['radiobutton']['bg']
RADIOBUTTON_FOREGROUND = STYLE['radiobutton']['fg']
RADIOBUTTON_RELIEF = STYLE['radiobutton']['relief']

# Checkbutton
CHECKBUTTON_FONT = (
    STYLE['checkbutton']['font']['family'], STYLE['checkbutton']['font']['size'], STYLE['checkbutton']['font']['style']
)
CHECKBUTTON_BACKGROUND = STYLE['checkbutton']['bg']
CHECKBUTTON_FOREGROUND = STYLE['checkbutton']['fg']
CHECKBUTTON_RELIEF = STYLE['checkbutton']['relief']

# Directories
OUTPUT_FILES_DIRECTORY_NAME = 'output_files'
OUTPUT_FILES_DIRECTORY = os.path.join(BASE_DIR, OUTPUT_FILES_DIRECTORY_NAME)
