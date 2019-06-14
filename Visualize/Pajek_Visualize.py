import re
from os_recon.define_os import path_escape


class PajekVisualize:
    """ This class creates a .net file from either an adjacency matrix or an adjacency list. """

    @staticmethod
    def pajek_visualize_matrix():
        file_output = ''
        with open(f"Output_Files{path_escape}Visualized_Graph.net", "w") as pajek_file:

            try:
                with open(f"Output_Files{path_escape}matrix.txt") as f:
                    # Number of Vertices

                    vertices = len(f.readline().replace("\n", ""))
                    f.seek(0)

                    file_output += f"*Vertices {vertices}\n"
                    for i in range(0, int(vertices)):
                        file_output += f'  {i + 1} "v{i + 1}"\n'

                    file_output += "*Edges\n"
                    i = 1
                    j = 1
                    for line in f:
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
                with open(f"Output_Files{path_escape}list.txt", buffering=20000) as f:
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
