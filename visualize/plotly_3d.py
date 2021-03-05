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
from os.path import join

import plotly
import igraph as ig
import plotly.plotly as py
import plotly.graph_objs as go
from tkinter import messagebox

from conf.base import OUTPUT_FILES_DIRECTORY
from graphs.graph import GraphRepresentationType
from os_recon.define_os import path_escape
from support_folders.run_length_encoder import RunLengthEncoder
from utils.file import locate_latest_file


class Plotly3D:

    def __init__(self, edges_pixels=1):
        self.link = None
        self.edges_pixels = edges_pixels

    def plotly_visualize_matrix(self, username, api_key, output_filename):
        global f

        # Plotly Credentials
        try:

            plotly.tools.set_credentials_file(username=username, api_key=api_key)

        except Exception as e:
            messagebox.showerror("Error!", e)
            return False

        # Create a list with all the connections between the nodes with source file: matrix.txt
        try:
            with open(join(OUTPUT_FILES_DIRECTORY,
                           f"{locate_latest_file(OUTPUT_FILES_DIRECTORY, GraphRepresentationType.MATRIX.value)}"),
                      buffering=20000) as f:
                # Number of Vertices
                encoder = RunLengthEncoder()
                line = f.readline()

                vertices = len(encoder.decode(line.replace('\n', ''))
                               if any(_ in [chr(0), chr(1)] for _ in line)
                               else line.replace("\n", ""))
                f.seek(0)

                i = 0
                j = 0
                Edges = []
                for line in f:
                    line = encoder.decode(line.replace('\n', '')) \
                        if any(_ in [chr(0), chr(1)] for _ in line) else line
                    for char in line:
                        if str(char) == '1' and i < j and i != j:
                            Edges.append((i, j))
                        j += 1
                    j = 0
                    i += 1

            # Create a list with all node names
            Nodes = [i for i in range(1, int(vertices) + 1)]

            # print(Edges)
            # print(Nodes)

            # Create a graph based on igraph library --> Graph Class.
            G = ig.Graph(len(Nodes), Edges, directed=False)

            # Create the appropriate labels for the nodes
            # labels = []
            # # group=[]
            # for name in Nodes:
            #     labels.append(name)
            #     # group.append(node['group'])

            labels = [f'v{name}' for name in Nodes]

            # Define Graph layout
            layt = G.layout('kk', dim=3)

            # Set the appropriate spawn coordinates for each node and edge
            N = len(Nodes)
            Xn = [layt[k][0] for k in range(N)]  # x-coordinates of nodes
            Yn = [layt[k][1] for k in range(N)]  # y-coordinates
            Zn = [layt[k][2] for k in range(N)]  # z-coordinates
            Xe = []
            Ye = []
            Ze = []
            for e in Edges:
                Xe += [layt[e[0]][0], layt[e[1]][0], None]  # x-coordinates of edge ends
                Ye += [layt[e[0]][1], layt[e[1]][1], None]
                Ze += [layt[e[0]][2], layt[e[1]][2], None]

            # Create a 3d Scatter plot for the edges
            trace1 = go.Scatter3d(x=Xe,
                                  y=Ye,
                                  z=Ze,
                                  mode='lines',
                                  line=dict(color='rgb(125,125,125)', width=self.edges_pixels),  # Edges color
                                  hoverinfo='none'
                                  )

            # Create a 3d Scatter plot for the nodes
            trace2 = go.Scatter3d(x=Xn,
                                  y=Yn,
                                  z=Zn,
                                  mode='markers',
                                  name='actors',
                                  marker=dict(symbol='circle',
                                              size=6,
                                              color="Black",  # Nodes color
                                              # colorscale='Viridis',
                                              line=dict(color='rgb(50,50,50)', width=0.5)
                                              ),
                                  text=labels,
                                  hoverinfo='text'
                                  )

            # Configure the axis
            axis = dict(showbackground=False,
                        showline=False,
                        zeroline=False,
                        showgrid=False,
                        showticklabels=False,
                        title=''
                        )

            # Configure the web-plot layout
            layout = go.Layout(
                title="3D visualization",
                width=1000,
                height=1000,
                showlegend=False,
                scene=dict(
                    xaxis=dict(axis),
                    yaxis=dict(axis),
                    zaxis=dict(axis),
                ),
                margin=dict(
                    t=100
                ),
                hovermode='closest',
                annotations=[
                    dict(
                        showarrow=False,
                        text="",
                        xref='paper',
                        yref='paper',
                        x=0,
                        y=0.1,
                        xanchor='left',
                        yanchor='bottom',
                        font=dict(
                            size=14
                        )
                    )
                ], )

            # Merge edges and nodes coordinates and create the 3d plot
            data = [trace1, trace2]
            fig = go.Figure(data=data, layout=layout)

            try:
                self.link = py.plot(fig, filename=output_filename, auto_open=False)

                return True

            except Exception as e:
                message = "User credentials were invalid!\nDon't have an account? " \
                          "You can always visit https://plot.ly/feed/#/ and create a new account."
                messagebox.showerror("Error!", message)
                return e

        except FileNotFoundError:
            return "File not found"

    def plotly_visualize_list(self, username, api_key, output_filename):

        global f

        # Plotly Credentials

        try:

            plotly.tools.set_credentials_file(username=username, api_key=api_key)

        except Exception as e:
            messagebox.showerror("Error!", e)
            return False

        # Create a list with all the connections between the nodes with source file: list.txt
        try:
            with open(join(OUTPUT_FILES_DIRECTORY,
                           f"{locate_latest_file(OUTPUT_FILES_DIRECTORY, GraphRepresentationType.LIST.value)}"),
                      buffering=20000) as f:
                # Number of Vertices
                vertices = int(f.readlines()[-1].split(':')[0]) + 1
                f.seek(0)

                Edges = []
                for i in range(vertices):
                    node_neighbors = f.readline().split(':')

                    node = node_neighbors[0]
                    neighbors = re.findall(r'[\d]+', node_neighbors[1])

                    Edges += [(int(node), int(neighbor)) for neighbor in neighbors]

            # Create a list with all node names
            Nodes = [i for i in range(1, int(vertices) + 1)]

            # print(Edges)
            # print(Nodes)

            # Create a graph based on igraph library --> Graph Class.
            G = ig.Graph(len(Nodes), Edges, directed=False)

            # Create the appropriate labels for the nodes
            # labels = []
            # # group=[]
            # for name in Nodes:
            #     labels.append(name)
            #     # group.append(node['group'])

            labels = [f'v{name}' for name in Nodes]

            # Define Graph layout
            layt = G.layout('kk', dim=3)

            # Set the appropriate spawn coordinates for each node and edge
            N = len(Nodes)
            Xn = [layt[k][0] for k in range(N)]  # x-coordinates of nodes
            Yn = [layt[k][1] for k in range(N)]  # y-coordinates
            Zn = [layt[k][2] for k in range(N)]  # z-coordinates
            Xe = []
            Ye = []
            Ze = []
            for e in Edges:
                Xe += [layt[e[0]][0], layt[e[1]][0], None]  # x-coordinates of edge ends
                Ye += [layt[e[0]][1], layt[e[1]][1], None]
                Ze += [layt[e[0]][2], layt[e[1]][2], None]

            # Create a 3d Scatter plot for the edges
            trace1 = go.Scatter3d(x=Xe,
                                  y=Ye,
                                  z=Ze,
                                  mode='lines',
                                  line=dict(color='rgb(125,125,125)', width=self.edges_pixels),  # Edges color
                                  hoverinfo='none'
                                  )

            # Create a 3d Scatter plot for the nodes
            trace2 = go.Scatter3d(x=Xn,
                                  y=Yn,
                                  z=Zn,
                                  mode='markers',
                                  name='actors',
                                  marker=dict(symbol='circle',
                                              size=6,
                                              color="Black",  # Nodes color
                                              # colorscale='Viridis',
                                              line=dict(color='rgb(50,50,50)', width=0.5)
                                              ),
                                  text=labels,
                                  hoverinfo='text'
                                  )

            # Configure the axis
            axis = dict(showbackground=False,
                        showline=False,
                        zeroline=False,
                        showgrid=False,
                        showticklabels=False,
                        title=''
                        )

            # Configure the web-plot layout
            layout = go.Layout(
                title="3D visualization",
                width=1000,
                height=1000,
                showlegend=False,
                scene=dict(
                    xaxis=dict(axis),
                    yaxis=dict(axis),
                    zaxis=dict(axis),
                ),
                margin=dict(
                    t=100
                ),
                hovermode='closest',
                annotations=[
                    dict(
                        showarrow=False,
                        text="",
                        xref='paper',
                        yref='paper',
                        x=0,
                        y=0.1,
                        xanchor='left',
                        yanchor='bottom',
                        font=dict(
                            size=14
                        )
                    )
                ], )

            # Merge edges and nodes coordinates and create the 3d plot
            data = [trace1, trace2]
            fig = go.Figure(data=data, layout=layout)

            try:

                self.link = py.plot(fig, filename=output_filename, auto_open=False)

                return True

            except Exception as e:
                message = "User credentials were invalid!\nDon't have an account? " \
                          "You can always visit https://plot.ly/feed/#/ and create a new account."
                messagebox.showerror("Error!", message)
                return e

        except FileNotFoundError:
            return "File not found"
