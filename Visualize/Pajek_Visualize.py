import re
from os_recon.define_os import path_escape


class Pajek_Visualize:

    @staticmethod
    def pajek_visualize_matrix():
        pajek_file = open("Output_Files{}Visualized_Graph.net".format(path_escape), "w")

        try:
            with open("Output_Files{}matrix.txt".format(path_escape), buffering=20000) as f:
                # Number of Vertices
                first_row = f.readline()
                counter = 0
                for char in first_row:
                    if char != "\n":
                        counter += 1
                Vertices = counter
                f.seek(0)
                # ===============================================

                pajek_file.write("*Vertices {}\n".format(Vertices))
                for i in range(0, int(Vertices)):
                    pajek_file.write('  {} "v{}"\n'.format(i + 1, i + 1))

                pajek_file.write("*Edges\n")

                i = 1
                j = 1
                for line in f:
                    for char in line:
                        if str(char) == '1' and i < j:
                            pajek_file.write("  {} {}\n".format(i, j))
                        j += 1
                    j = 1
                    i += 1

                f.close()
                pajek_file.close()

            return True
        except FileNotFoundError:
            pajek_file.close()
            return False

    @staticmethod
    def pajek_visualize_list():
        pajek_file = open("Output_Files{}Visualized_Graph.net".format(path_escape), "w")

        try:
            with open("Output_Files{}list.txt".format(path_escape), buffering=20000) as f:
                # Number of Vertices
                Vertices = int(f.readlines()[-1].split(':')[0]) + 1
                f.seek(0)
                # ===============================================

                pajek_file.write("*Vertices {}\n".format(Vertices))
                for i in range(0, Vertices):
                    pajek_file.write('  {} "v{}"\n'.format(i + 1, i + 1))

                pajek_file.write("*Edges\n")

                for i in range(Vertices):
                    node = f.readline().split(':')[1]

                    neighbors = re.findall(r'(\d*[^,\n])', node)
                    for neighbor in neighbors:
                        try:
                            if i != int(neighbor) and i < int(neighbor):
                                pajek_file.write("  {} {}\n".format(i + 1, int(neighbor) + 1))
                        except ValueError:
                            pass

                f.close()
                pajek_file.close()

            return True
        except FileNotFoundError:
            pajek_file.close()
            return False


Visualizer = Pajek_Visualize()
