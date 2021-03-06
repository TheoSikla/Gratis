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
from conf.general import STYLES_PATH

with open(STYLES_PATH) as f:
    try:
        STYLES = json.load(f)
    except Exception:
        exit(1)

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

# Label
LABEL_FONT_LARGE = (
    STYLE['label']['font']['family'], STYLE['label']['font']['size']['large'], STYLE['label']['font']['style']
)
LABEL_FONT_MEDIUM = (
    STYLE['label']['font']['family'], STYLE['label']['font']['size']['medium'], STYLE['label']['font']['style']
)
LABEL_BACKGROUND = STYLE['label']['bg']
LABEL_FOREGROUND = STYLE['label']['fg']
LABEL_RELIEF = STYLE['label']['relief']

# Scrollable frame
SCROLLABLE_FRAME_FONT = (
    STYLE['scrollable_frame']['font']['family'],
    STYLE['scrollable_frame']['font']['size'],
    STYLE['scrollable_frame']['font']['style']
)
SCROLLABLE_FRAME_BACKGROUND = STYLE['scrollable_frame']['bg']