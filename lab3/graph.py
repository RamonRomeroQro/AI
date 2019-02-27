from collections import deque


class GraphSearchSpace():
    def __init__(self):
        self.nodes = set()
     

        #n1_to_n2=Edge(node1, node2, o_stack, dest_stack)
        #n2_to_n1=Edge(node1, node2, dest_stack, o_stack)
        # self.edges.append(n1_to_n2)
        # self.edges.append(n2_to_n1)

    def __str__(self):
        # s=""
        # for i in self.nodes:
        #     s=s+i.__str__()+"\n"
        # return s
        s = ""
        for i in self.nodes:
            s = s+i.__str__()+"\n"

        return s


class Edge():

    def __init__(self, node2, o_stack, dest_stack):
        self.destination = node2
        self.origin_stack = o_stack
        self.destination_stack = dest_stack
        # Example: moving a container from stack 2 to stack 4 takes 0.5 + abs(2 - 4) + 0.5 = 3 minutes.
        self.cost = 1+abs(o_stack-dest_stack)


    def __str__(self):
       return (f'--({self.cost}, {self.origin_stack}, {self.destination_stack})--> ')+str(self.destination)

    def __eq__(self, other):
        if isinstance(other, Edge):
            return ((self.destination == other.destination) and (self.origin_stack == other.origin_stack) and (self.destination_stack == other.destination_stack) and (self.cost == other.cost))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash((self.cost, self.destination_stack, self.origin_stack, self.destination))


class Node:

    def add_conection(self, n2, o_stack, dest_stack):
        c = Edge(n2, o_stack, dest_stack)
        self.conections.add(c)

    def __str__(self):
        return self.structure.__str__()

    def __eq__(self, other):
        if isinstance(other, Node):
            return ((self.structure == other.structure))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(tuple(map(tuple, self.structure)))

    def __init__(self, structure, h):
        self.num_stacks = len(structure)
        self.max_height = h
        self.structure = structure
        self.conections = set()

    def generate_paths(self, gsp):
        # print('genfor',self.structure)
        #for i in range(0, self.num_stacks):
        #   for j in range(0, self.num_stacks):
        #        self.transition_model(i, j, gsp)

        q=deque([i for i in range(0,self.num_stacks)])
        for i in range(0,self.num_stacks):
            e=q.popleft()
            q.append(e)
            for j in range(1+i,len(q)):
        #         #print(i,j)
                self.transition_model(i,j,gsp)
                self.transition_model(j,i,gsp)

    def transition_model(self, origin_stack, destination_stack, gsp):
        if len(self.structure[destination_stack])+1 <= self.max_height and (len(self.structure[origin_stack])-1) >= 0:
            new_structure = list(map(list, self.structure))
            e = new_structure[origin_stack].pop()
            new_structure[destination_stack].append(e)
            new_node = Node(new_structure, self.max_height)

            gsp.nodes.add(self)

            evaluation_set=set()
            evaluation_set.add(new_node)
            evaluation_set=evaluation_set.intersection(gsp.nodes)
            if len(evaluation_set)==0:
                gsp.nodes.add(new_node)
                # conect to new
                #print(self.structure,'\t->\t', new_node.structure)
                #gsp.add_conection(self, new_node, origin_stack, destination_stack)
                self.add_conection(new_node, origin_stack, destination_stack)
                new_node.generate_paths(gsp)
            else:
                for i in evaluation_set:
                    self.add_conection(i, origin_stack, destination_stack)


def main():
    '''
    max_height = int(input())
    start_structure = str(input())
    goal_structure = str(input())
    start_structure = start_structure.strip().split(";")
    goal_structure = goal_structure.strip().split(";")
    start_structure = list(map(lambda x: x.strip().strip("(").strip(")"), start_structure))
    goal_structure = list(map(lambda x: x.strip().strip("(").strip(")"), goal_structure))
    start_structure = list(map(lambda x: x.split(", ") if x != "X" else [], start_structure))
    goal_structure = list(map(lambda x: x.split(", ") if x != "X" else [], goal_structure))
    print(goal_structure)
    print(start_structure)
    gsp=GraphSearchSpace()
    initialState = Node(start_structure, max_height)
    initialState.generate_paths(gsp)
    '''

    max_height = 2
    goal_structure = [['A', 'C'], [], []]
    start_structure = [['A'], ['B'], ['C']]
    gsp = GraphSearchSpace()
    initialState = Node(start_structure, max_height)
    # a=set()
    # a.add(initialState)
    # second = Node(start_structure, max_height)
    # print(second in a)



    initialState.generate_paths(gsp)
    #print("kmkm")
    print(gsp.__str__())
    for i in initialState.conections:
        print(i)


if __name__ == "__main__":
    main()


#import fileinput

#lines = []
# for line in fileinput.input():
#    lines.append(line.strip())
# num=list(map(int,lines[0]))[0]
# print(sum(num))

'''

def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar
    def __repr__(self):
        return "Item(%s, %s)" % (self.foo, self.bar)
    def __eq__(self, other):
        if isinstance(other, Item):
            return ((self.foo == other.foo) and (self.bar == other.bar))
        else:
            return False
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        return hash(self.__repr__())



class SearchSpace():
    def __init__(self):
        self.nodes = set()
        self.edges = set()


class Node:

    def __init__(self, structure, h):
        self.num_stacks = len(structure)
        self.max_height = h
        self.structure = structure

#   def looking_transition(self. origin_stack, destination_stack):



def main():

    a = int(input())
    start = str(input())
    goal = str(input())
    start = start.strip().split(";")
    goal = goal.strip().split(";")
    start = list(map(lambda x: x.strip().strip("(").strip(")"), start))
    goal = list(map(lambda x: x.strip().strip("(").strip(")"), goal))
    start = list(map(lambda x: x.split(", ") if x != "X" else [], start))
    goal = list(map(lambda x: x.split(", ") if x != "X" else [], goal))
    print(start)
    print(goal)
    

from collections import deque

def generate_iterations(size_structure):
    q=deque([i for i in range(0,size_structure)])
    for i in range(0,size_structure):
        e=q.popleft()
        q.append(e)
        for j in range(1+i,len(q)):
            print(i,j)
        
        
  
    generate_iterations(4) 
    
'''
