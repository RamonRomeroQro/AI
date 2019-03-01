'''
    Copyright 2019 © Ramón Romero @ramonromeroqro
    Intelligent Systems, ITESM.
    A01700318 for ITESM

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''


from collections import deque
import copy


class GraphSearchSpace():
    def __init__(self, m_h,):
        self.nodes = {}
        self.heuristic = {}
        self.max_height = m_h

    def generate_heuristic(self, goal_structure):
        for k, v in self.nodes.items():
            m1f = copy.deepcopy(v.structure)
            m2f = copy.deepcopy(goal_structure)
            m1f = self.filling(m1f)
            m2f = self.filling(m2f)
            #print('->>', v.structure,m1f )

            self.heuristic[k] = self.evaluate(m1f, m2f)

    def evaluate(self, m1, m2):
        s = 0
        for i in range(len(m1)):
            for j in range(self.max_height):
                if m1[i][j] == m2[i][j] and m1[i][j] != "*":
                    s = s+1
        return s

    def filling(self, mat):
        for s in mat:
            if len(s) < self.max_height:
                for i in range(0, abs(len(s)-self.max_height)):
                    s.append('*')
        return mat

    def __str__(self):

        s = ""
        for i in self.nodes:
            s = s+i.__str__()+"\n"

        return s


class Node:

    def __str__(self):
        return str(self.id)

    def __init__(self, structure):
        self.num_stacks = len(structure)
        self.structure = structure
        self.conections = {}
        self.id = tuple(map(tuple, self.structure))

    def generate_node(self, origin_stack, destination_stack, gsp):
        if len(self.structure[destination_stack])+1 <= gsp.max_height and (len(self.structure[origin_stack])-1) >= 0:
            new_structure = list(map(list, self.structure))
            e = new_structure[origin_stack].pop()
            new_structure[destination_stack].append(e)
            new_node = Node(new_structure)
            return new_node

        else:
            return None

    def generate_paths(self, gsp):
        execution_queue = deque([])
        gsp.nodes[self.id] = self
        execution_queue.append(self)
        while(len(execution_queue)):
            ex_node = execution_queue.popleft()
            for i in range(0, ex_node.num_stacks):
                for j in range(0, ex_node.num_stacks):
                    if i != j:
                        new_node = ex_node.generate_node(i, j, gsp)
                        cost = 1+abs(i-j)
                        if (new_node != None):
                            if new_node.id not in gsp.nodes:
                                gsp.nodes[new_node.id] = new_node
                                ex_node.conections[(
                                    i, j, cost)] = gsp.nodes[new_node.id]
                                execution_queue.append(new_node)
                            else:
                                existent_node = gsp.nodes[new_node.id]
                                ex_node.conections[(
                                    i, j, cost)] = existent_node


def ucs(start_node, goal_node):
    explored = {}
    pq = PriorityQueue()
    # nodo, currentsume, path, heuristica
    pq.add((start_node, 0, [], 0))
    while(True):
        # print(str(pq))
        if pq.is_empty() == True:
            return "No solution found"
        nodo, latest_cost, path = pq.pop()
        #print("...", path)
        if nodo.id == goal_node.id:
            explored[nodo.id] = nodo
            # print(cost, nodo)
            # print(path)
            # print(latest_cost)
            return str(latest_cost)+"\n"+"; ".join([str(x) for x in (path)])
        # print("expanded ___!", nodo, cost)
        for t, n in nodo.conections.items():  # expansion
            conex = n
            cost_n = t[2]
            trans = (t[0], t[1])
            n_path = list(path)
            # print(n_path)
            n_path.append(trans)
            if conex.id not in explored:  # or conex not frontier:
                # print(conex)
                pq.add((conex, cost_n+latest_cost, n_path, 0))


def a_star(start_node, goal_node, gsp):
    explored = {}
    pq = PriorityQueue()
    # nodo, currentsume, path, heuristica
    pq.add((start_node, 0, [], gsp.heuristic[start_node.id]))
    while(True):
        # print(str(pq))
        if pq.is_empty() == True:
            return "No solution found"
        nodo, latest_cost, path = pq.pop()
        #print("...", path)
        if nodo.id == goal_node.id:
            explored[nodo.id] = nodo
            # print(cost, nodo)
            # print(path)

            # print(latest_cost)
            return str(latest_cost)+"\n"+"; ".join([str(x) for x in (path)])
        # print("expanded ___!", nodo, cost)
        for t, n in nodo.conections.items():  # expansion
            conex = n
            cost_n = t[2]
            trans = (t[0], t[1])
            n_path = list(path)
            # print(n_path)
            n_path.append(trans)

            if conex.id not in explored:  # or conex not frontier:
                # print(conex)
                pq.add((conex, cost_n+latest_cost,
                        n_path, gsp.heuristic[conex.id]))


def greedy_evaluation(m1, g):
    for i in range(len(g)):
        if g[i] != ['X'] and m1[i] != g[i]:
            return False
    return True


def greedy_ucs(start_node, goal_node):
    explored = {}
    pq = PriorityQueue()
    # nodo, currentsume, path, heuristica
    pq.add((start_node, 0, [], 0))
    while(True):
        # print(str(pq))
        if pq.is_empty() == True:
            return "No solution found"
        nodo, latest_cost, path = pq.pop()
        #print("...", path)
        #print(greedy_evaluation(nodo.structure, goal_node.structure))
        if (greedy_evaluation(nodo.structure, goal_node.structure) == True):
            explored[nodo.id] = nodo
            # print(cost, nodo)
            # print(path)

            # print(latest_cost)
            return str(latest_cost)+"\n"+"; ".join([str(x) for x in (path)])
        # print("expanded ___!", nodo, cost)
        for t, n in nodo.conections.items():  # expansion
            conex = n
            cost_n = t[2]
            trans = (t[0], t[1])
            n_path = list(path)
            # print(n_path)
            n_path.append(trans)

            if conex.id not in explored:  # or conex not frontier:
                # print(conex)
                pq.add((conex, cost_n+latest_cost, n_path, 0))


def greedy_a_star(start_node, goal_node, gsp):
    explored = {}
    pq = PriorityQueue()
    # nodo, currentsume, path, heuristica
    pq.add((start_node, 0, [], gsp.heuristic[start_node.id]))
    while(True):
        # print(str(pq))
        if pq.is_empty() == True:
            return "No solution found"
        nodo, latest_cost, path = pq.pop()
        #print("...", path)
        #print((nodo.structure, goal_node.structure))

        if greedy_evaluation(nodo.structure, goal_node.structure) == True:
            explored[nodo.id] = nodo
            # print(cost, nodo)
            # print(path)

            # print(latest_cost)
            return str(latest_cost)+"\n"+"; ".join([str(x) for x in (path)])
        # print("expanded ___!", nodo, cost)
        for t, n in nodo.conections.items():  # expansion
            conex = n
            cost_n = t[2]
            trans = (t[0], t[1])
            n_path = list(path)
            # print(n_path)
            n_path.append(trans)

            if conex.id not in explored:  # or conex not frontier:
                # print(conex)
                pq.add((conex, cost_n+latest_cost,
                        n_path, gsp.heuristic[conex.id]))


class PriorityQueue():

    def is_empty(self):
        if len(self.q) == 0:
            return True
        return False

    def __init__(self):
        self.q = deque([])

    def __str__(self):
        s = "\n-----------\n"
        for i in self.q:
            s = s+str(i[0])+", "+str(i[1])+";\n"
        return s

    def pop(self):
        self.q = deque(self.q)
        a = self.q.popleft()
        return a[0], a[1], (a[2])

    def add(self, paired):
        self.q.append(paired)
        self.q = sorted(self.q, key=lambda x: (x[1]+x[3]))


def main():
    # PARSING INPUT
    max_height = int(input())
    start_structure = str(input())
    goal_structure = str(input())
    start_structure = start_structure.strip().split(";")
    goal_structure = goal_structure.strip().split(";")
    start_structure = list(
        map(lambda x: x.strip().strip("(").strip(")"), start_structure))
    goal_structure = list(
        map(lambda x: x.strip().strip("(").strip(")"), goal_structure))
    start_structure = list(map(lambda x: x.split(
        ", ") if x != '' else [], start_structure))
    goal_structure = list(map(lambda x: x.split(
        ", ") if x != '' else [], goal_structure))

    # DEBUG PAARSING
    # print('G?->', goal_structure)
    # print('S?->', start_structure)
    # Initial Node Creation

    # Dummy Node for Debug
    # max_height = 2
    # goal_structure = [['A', 'C'], [], []]
    # start_structure = [['A'], ['B'], ['C']]

    # Graph Search Space Creation
    gsp = GraphSearchSpace(max_height)
    initialState = Node(start_structure)
    goalState = Node(goal_structure)
    initialState.generate_paths(gsp)

    greedy = False
    for l in goal_structure:
        for i in l:
            if i == "X":
                greedy = True
                break
    # print(greedy)

    # Execute generation of path for Initial node

    if greedy == True:
        print(greedy_ucs(initialState, goalState))
        # gsp.generate_heuristic(goalState.structure)
        #print(greedy_a_star(initialState, goalState, gsp))

    else:
        if goalState.id in gsp.nodes:
            print(ucs(initialState, goalState))
            # gsp.generate_heuristic(goalState.structure)
            #print(a_star(initialState, goalState, gsp))
        else:
            print("No solution found")

        #print(a_star(initialState, goalState))

    # for k,v in initialState.conections.items():
    #   print(k,v )

    # print(initialState)

    # print("kmkm")
    # print(gsp.__str__())
    # for i in initialState.conections:
    # print(i)


if __name__ == "__main__":
    main()

#import fileinput

#lines = []
# for line in fileinput.input():
#    lines.append(line.strip())
# num=list(map(int,lines[0]))[0]
# print(sum(num))
