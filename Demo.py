import time


from IVAStar.IVGraph import IVGraph
from IVAStar.IVGraph import IVGraphNode
from IVAStar.IVGraph import IVAStar
import random



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start = time.time()
    iterations_max = 30
    iterations = 0
    string_length = 0
    runtimes = []
    N_ints = []
    lengths = []
    input_list = []
    output = []
    max_blockers = 3
    graph_width = 20
    graph_height = 10
    blocker_max_width = 4
    blocker_max_height = 8

    input = IVGraph(graph_height, graph_width, 1)


    blocker_height = graph_height * 2
    blocker_width = 1
    blocker_offset_x = graph_width / 2
    blocker_offset_y = graph_height
    blocker_x = blocker_offset_x
    blocker_y = blocker_offset_y
    input.place_blocker(blocker_width, blocker_height, blocker_x, blocker_y, 0)

    input_list.append(input)
    N = len(input.nodes)
    N_ints.append(N)
    start = time.time()
    output.append(IVAStar(input.nodes[10][4], input.nodes[15][15], input, False))
    end = time.time()
    executionTime = (end - start)
    runtimes.append(executionTime)

    for i in range(iterations_max):

        input = IVGraph(graph_height, graph_width, 1)
        num_blockers = random.randint(0, max_blockers)
        for blocker_idx in range(num_blockers):
            blocker_height = random.randint(3, blocker_max_height)
            blocker_width = random.randint(3, blocker_max_width)
            blocker_x = random.randint(0, graph_width)
            blocker_y = random.randint(0, graph_height)
            input.place_blocker(blocker_width, blocker_height, blocker_x, blocker_y, 0)
        for blocker_idx in range(num_blockers):
            blocker_height = random.randint(3, blocker_max_height)
            blocker_width = random.randint(3, blocker_max_width)
            blocker_x = random.randint(0, graph_width)
            blocker_y = random.randint(0, graph_height)
            input.place_blocker(blocker_width, blocker_height, blocker_x, blocker_y, random.randint(2,3))
        input_list.append(input)
        N = len(input.nodes)
        N_ints.append(N)
        start = time.time()
        output.append(IVAStar(input.nodes[10][4], input.nodes[15][15], input, False))
        end = time.time()
        executionTime = (end - start)
        runtimes.append(executionTime)
        #print("Input: " + input + " Output: " + str(output[i]))




