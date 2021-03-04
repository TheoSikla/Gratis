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

from graphs.graph import GraphRepresentationType
from os_recon.define_os import path_escape
from support_folders.run_length_encoder import RunLengthEncoder
from utils.file import locate_latest_file


class PajekVisualize:
    """ This class creates a .net file from either an adjacency matrix or an adjacency list. """

    @staticmethod
    def pajek_visualize_matrix():
        file_output = ''
        with open(f"Output_Files{path_escape}Visualized_Graph.net", "w") as pajek_file:

            try:
                with open(f"Output_Files{path_escape}"
                          f"{locate_latest_file('Output_Files', GraphRepresentationType.MATRIX.value)}",
                          buffering=20000) as f:
                    # Number of Vertices

                    encoder = RunLengthEncoder()
                    line = f.readline()

                    vertices = len(encoder.decode(line.replace('\n', ''))
                                   if any(_ in [chr(0), chr(1)] for _ in line)
                                   else line.replace("\n", ""))
                    f.seek(0)

                    file_output += f"*Vertices {vertices}\n"
                    for i in range(0, int(vertices)):
                        file_output += f'  {i + 1} "v{i + 1}"\n'

                    file_output += "*Edges\n"
                    i = 1
                    j = 1
                    for line in f:
                        line = encoder.decode(line.replace('\n', '')) \
                            if any(_ in [chr(0), chr(1)] for _ in line) else line
                        for char in line:
                            if char == '1' and i < j:
                                file_output += f"  {i} {j}\n"
                            j += 1
                        j = 1
                        i += 1

                pajek_file.write(file_output)
                del file_output
                return True
            except FileNotFoundError:
                return False

    @staticmethod
    def pajek_visualize_list():
        file_output = ''
        with open(f"Output_Files{path_escape}Visualized_Graph.net", "w") as pajek_file:

            try:
                with open(f"Output_Files{path_escape}"
                          f"{locate_latest_file('Output_Files', GraphRepresentationType.LIST.value)}",
                          buffering=20000) as f:
                    # Number of Vertices
                    vertices = int(f.readlines()[-1].split(':')[0]) + 1
                    f.seek(0)

                    # ===============================================

                    file_output += f"*Vertices {vertices}\n"
                    for i in range(0, vertices):
                        file_output += f'  {i + 1} "v{i + 1}"\n'

                    file_output += "*Edges\n"

                    for i in range(vertices):
                        neighbors = re.findall(r'(\d*[^,\n])', f.readline().split(':')[1])
                        if len(neighbors) > 0:
                            for neighbor in neighbors:
                                if i < int(neighbor):
                                    file_output += f"  {i + 1} {int(neighbor) + 1}\n"

                pajek_file.write(file_output)
                del file_output
                return True
            except FileNotFoundError:
                return False


Visualizer = PajekVisualize()
