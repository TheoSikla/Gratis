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

import sys
from tkinter import ttk, Label

from conf.base import MAIN_FRAME_BACKGROUND, GENERATE_AREA_BUTTON_TEXT, ANALYZE_AREA_BUTTON_TEXT, \
    VISUALIZE_AREA_BUTTON_TEXT, HISTORY_AREA_BUTTON_TEXT, EXIT_BUTTON_TEXT, MAIN_WINDOW_DIMENSIONS_STR
from gui.pages.page import Page


class MainPage(Page):

    def __init__(self, parent, controller):
        super(MainPage, self).__init__(parent)

        # MainPage Frame configuration
        self.configure(bg=MAIN_FRAME_BACKGROUND)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(7, weight=1)

        # Button configuration variables
        self.ipady = 10

        # Main Label
        self.main_label = Label(self, bg="azure3", text="Welcome to Graph Sphere\n",
                                font=("Arial", 20, "bold"))
        # self.main_label.grid(row=1, column=1, columnspan=3)

        # Generate area button
        self.generate_area = ttk.Button(self, text=GENERATE_AREA_BUTTON_TEXT,
                                        command=lambda: controller.show_frame(
                                            self.retrieve_frame(controller, 'GraphGeneratePage'),
                                            MAIN_WINDOW_DIMENSIONS_STR))
        self.generate_area.grid(row=2, column=1, ipady=self.ipady, padx=30)

        # Analyze area button
        self.analyze_area = ttk.Button(self, text=ANALYZE_AREA_BUTTON_TEXT,
                                       command=lambda: controller.show_frame(
                                           self.retrieve_frame(controller, 'GraphAnalyzePage'),
                                           MAIN_WINDOW_DIMENSIONS_STR)
                                       )
        self.analyze_area.grid(row=2, column=2, ipady=self.ipady, padx=30)

        # Visualize area button
        self.visualise_area = ttk.Button(self, text=VISUALIZE_AREA_BUTTON_TEXT,
                                         command=lambda: controller.show_frame(
                                             self.retrieve_frame(controller, 'GraphVisualizePage'),
                                             MAIN_WINDOW_DIMENSIONS_STR)
                                         )
        self.visualise_area.grid(row=2, column=3, ipady=self.ipady, padx=30)

        # Graph History area button
        self.graph_history_area = ttk.Button(self, text=HISTORY_AREA_BUTTON_TEXT,
                                             command=lambda: [controller.show_frame(
                                                 self.retrieve_frame(controller, 'GraphHistoryPage'),
                                                 MAIN_WINDOW_DIMENSIONS_STR
                                             ),
                                                 controller.frames[
                                                     self.retrieve_frame(controller, 'GraphHistoryPage')
                                                 ].fecth_fresh_data()]
                                             )
        self.graph_history_area.grid(row=2, column=4, ipady=self.ipady, padx=30)

        # Exit button
        self.exit = ttk.Button(self, text=EXIT_BUTTON_TEXT, command=lambda: sys.exit(0))
        self.exit.grid(row=3, column=4, ipady=self.ipady, pady=20)
