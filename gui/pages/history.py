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
from gui.pages.page import *


class GraphHistoryPage(Page):
    def __init__(self, parent, controller):
        super(GraphHistoryPage, self).__init__(parent)

        self.parent = parent
        self.controller = controller

        self.configure(bg="azure3")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.graph_connection_handler = Graph()

        self.graphs = []
        self.graph_mini_frames = []
        self.graph_label_id = []
        self.buttons_frames = []
        self.delete_buttons = []
        self.more_buttons = []
        self.less_buttons = []
        self.load_counter = 0

        self.canvas = Canvas(self, borderwidth=0, background="azure3", highlightthickness=1,
                             highlightbackground="azure3")
        self.graphs_frame = Frame(self.canvas, background="azure3")
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview, bg="black")
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="news")
        self.canvas.create_window((4, 4), window=self.graphs_frame, anchor="nw",
                                  tags="self.graphs_frame")

        self.graphs_frame.bind("<Configure>", self.onFrameConfigure)

        MousewheelSupport(self).add_support_to(self.canvas, yscrollbar=self.vsb, what="units")

        self.back_button = ttk.Button(self, text="Back", command=lambda: self.back(self.controller))
        self.back_button.grid(row=1, column=0, ipady=10, ipadx=15, pady=10, sticky="e")

    def scroll_possition_check(self):
        try:
            if self.vsb.get()[1] == 1.0 and len(self.graph_mini_frames) > 0:
                self.grid_data()
        except IndexError:
            if self.scroll_possition_check is not None:
                self.after_cancel(self.scroll_possition_check)
        self.after(200, self.scroll_possition_check)

    def grid_data(self):
        for i in range(self.load_counter, self.load_counter + 5):
            self.graph_mini_frames[i].grid(pady=10, padx=10, sticky="news")
            self.graph_label_id[i].grid(row=0, column=0, sticky="news")
            self.graphs[i].grid(row=0, column=1, sticky='nesw')
            self.buttons_frames[i].grid(row=0, column=2, sticky="news")
            self.delete_buttons[i].grid(row=0, column=0, sticky="n")
            self.more_buttons[i].grid(row=0, column=1, sticky="ne", padx=(0, 20))
            self.update()
            self.update_idletasks()
        self.load_counter += 5

    def data(self):
        graph_connection_handler = Graph()
        self.graph_objects = graph_connection_handler.all()
        counter = 0
        for graph in self.graph_objects:
            graph_contents = ''

            self.graph_mini_frames.append(
                Frame(self.graphs_frame, bg="azure3", height=77, borderwidth="1", relief="solid"))
            if platform_type == "Windows":
                self.graph_mini_frames[-1].config(width=900)
            else:
                self.graph_mini_frames[-1].config(width=1000)
            self.graph_mini_frames[-1].grid_propagate(False)
            self.graph_mini_frames[-1].rowconfigure(0, weight=1)
            self.graph_mini_frames[-1].columnconfigure(1, weight=1)

            self.graph_label_id.append(
                Label(self.graph_mini_frames[-1], text=f"{counter + 1}", bg="azure3", width=5, height=10,
                      font='Arial 18 bold'))
            self.graph_label_id[-1].grid_propagate(0)

            graph_contents += f"Generated at: {graph[2]}\n"

            for k, v in json.loads(graph[1]).items():
                graph_contents += f"{k.replace('_', ' ')}: {v}\n"

            self.graphs.append(
                Label(self.graph_mini_frames[-1], text=graph_contents, width=10, bg="azure3", justify="left",
                      anchor="nw", font='Arial 15'))

            self.buttons_frames.append(Frame(self.graph_mini_frames[-1], bg="azure3", width=300))
            self.buttons_frames[-1].grid_propagate(False)
            self.buttons_frames[-1].rowconfigure(0, weight=1)
            self.buttons_frames[-1].columnconfigure(0, weight=1)
            self.buttons_frames[-1].columnconfigure(1, weight=1)

            try:
                delete_graph = PhotoImage(file='./images{}delete.png'.format(path_escape))
                self.delete_buttons.append(Button(self.buttons_frames[-1], image=delete_graph, highlightthickness=1,
                                                  highlightbackground="azure3",
                                                  command=lambda x=(int(counter), graph[0]): self.delete_button_func(
                                                      x[0], x[1])))
                self.delete_buttons[-1].image = delete_graph
                self.delete_buttons[-1].config(bg='azure3', relief='sunken', borderwidth=0)

                more_graph = PhotoImage(file='./images{}down.png'.format(path_escape))
                self.more_buttons.append(
                    Button(self.buttons_frames[-1], image=more_graph, text=counter, highlightthickness=1,
                           highlightbackground="azure3", command=lambda x=int(counter): self.more_button_func(x)))
                self.more_buttons[-1].image = more_graph
                self.more_buttons[-1].config(bg='azure3', relief='sunken', borderwidth=0)

                less_graph = PhotoImage(file='./images{}up.png'.format(path_escape))
                self.less_buttons.append(
                    Button(self.buttons_frames[-1], image=less_graph, text=counter, highlightthickness=1,
                           highlightbackground="azure3", command=lambda x=int(counter): self.less_button_func(x)))
                self.less_buttons[-1].image = less_graph
                self.less_buttons[-1].config(bg='azure3', relief='sunken', borderwidth=0)
            except TclError:
                self.delete_buttons.append(Button(self.buttons_frames[-1], text='Delete',
                                                  command=lambda x=(int(counter), graph[0]): self.delete_button_func(
                                                      x[0], x[1])))
                self.delete_buttons[-1].config(bg='azure3', relief='sunken', borderwidth=1)
                self.more_buttons.append(Button(self.buttons_frames[-1], text='More',
                                                command=lambda x=int(counter): self.more_button_func(x)))
                self.more_buttons[-1].config(bg='azure3', relief='sunken', borderwidth=1)
                self.less_buttons.append(Button(self.buttons_frames[-1], text='Less',
                                                command=lambda x=int(counter): self.less_button_func(x)))
                self.less_buttons[-1].config(bg='azure3', relief='sunken', borderwidth=1)

            graph_contents = ''
            counter += 1
        graph_connection_handler.close()
        self.grid_data()

    def more_button_func(self, button_id):
        self.graph_mini_frames[button_id].configure(height=270)
        self.less_buttons[button_id].grid(row=0, column=1, sticky="ne", padx=(0, 20))

    def less_button_func(self, button_id):
        self.graph_mini_frames[button_id].configure(height=77)
        self.less_buttons[button_id].grid_forget()

    def delete_button_func(self, button_id, graph_id):
        if self.graph_connection_handler.delete(graph_id):
            self.graph_mini_frames[button_id].grid_forget()

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def back(self, controller):
        # self.canvas.yview_moveto(1)
        controller.show_frame(self.retrieve_frame(controller, 'MainPage'), transform)

    def clean_old_data(self):
        for frame in self.graph_mini_frames:
            frame.grid_forget()
        self.graphs.clear()
        self.graph_mini_frames.clear()
        self.graph_label_id.clear()
        self.buttons_frames.clear()
        self.delete_buttons.clear()
        self.more_buttons.clear()
        self.less_buttons.clear()
        self.load_counter = 0
        self.canvas.yview_moveto(0)

    def fecth_fresh_data(self):
        count = self.graph_connection_handler.count()
        frame_len = len(self.graph_mini_frames)
        if frame_len < count or frame_len > count:
            self.clean_old_data()
            self.data()
            self.scroll_possition_check()
