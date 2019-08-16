# Time efficient but not so friendly with memory
cpdef list generate_graph(int number_of_vertices):
    cdef int i, j
    cdef list arr=[]
    cdef list outout=[]

    for i in range(number_of_vertices):
        outout=[]
        for j in range(number_of_vertices):
            if i < j:
                outout.append(1)
            else:
                outout.append(0)
        arr.append(outout)
    return arr


# NOPE - not time efficient but memory saving
# import random
#
# cpdef list generate_graph_2(int number_of_vertices):
#     cdef int i, j, connection_choice, memory
#     cdef ones_counter = 0, zeros_counter = 0
#     cdef list arr=[]
#     cdef list outout=[]
#     # cdef str rand_str = ''
#
#     for i in range(number_of_vertices):
#         outout=[]
#         for j in range(number_of_vertices):
#             connection_choice = random.randint(0, 1)
#             # rand_str += str(connection_choice)
#             if j == 0:
#                 memory = connection_choice
#             if memory != connection_choice:
#                 if memory == 1:
#                     outout.append((ones_counter, 1))
#                     ones_counter = 0
#                     memory = 0
#                 else:
#                     outout.append((zeros_counter, 0))
#                     zeros_counter = 0
#                     memory = 1
#             if connection_choice == 1:  # If there is a connection
#                 ones_counter += 1
#             else:
#                 zeros_counter += 1
#
#             if j == number_of_vertices - 1:
#                 if memory == 1:
#                     outout.append((ones_counter, 1))
#                     ones_counter = 0
#                     memory = 0
#                 else:
#                     outout.append((zeros_counter, 0))
#                     zeros_counter = 0
#                     memory = 1
#         # print(rand_str)
#         # rand_str = ''
#         arr.append(outout)
#     return arr
