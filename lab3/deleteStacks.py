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
        
    def __init__(self):
        self.num_stacks = 0
        self.max_height = 0
        self.structure = []
        self.conections = set()
        

    def generate_paths(self, gsp):
        #print('genfor',self.structure)
        
        q=deque([i for i in range(0,self.num_stacks)])
        for i in range(0,self.num_stacks):
            e=q.popleft()
            q.append(e)
            for j in range(i,len(q)):
        # print(i,j)
                self.transition_model(i,j,gsp)

    def transition_model(self, origin_stack, destination_stack, gsp):

        
        if len(self.structure[destination_stack])+1 <= self.max_height and (len(self.structure[origin_stack])-1) >= 0:
           
            new_node=Node()
            if origin_stack==destination_stack and (len(self.structure[origin_stack])-1) >= 0:
                new_structure = list(map(list, self.structure))
                e = new_structure[origin_stack].pop()
                new_node.structure=new_structure
                new_node.max_height=self.max_height
            else:

                new_structure = list(map(list, self.structure))
                e = new_structure[origin_stack].pop()
                new_structure[destination_stack].append(e)
                new_node.structure=new_structure
                new_node.structure=self.max_height

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
                    #print("MM", len(evaluation_set))
                    self.add_conection(i, origin_stack, destination_stack)
                    #i.add_conection(self,destination_stack, origin_stack)


def ucs(start_node, goal_node):
    explored=set()
    pq=PriorityQueue()
    pq.add((start_node, 0))
    while(True):
        print(str(pq))
        if pq.is_empty()==True:
            return "failed"
        nodo, cost =pq.pop()
        if nodo==goal_node:
            explored.add(nodo)
            print(cost, nodo)
            return "founded"
        print("expanded ___!", nodo, cost)
        for i in nodo.conections: #expansion
            conex=i.destination
            cost_n=i.cost
            if conex not in explored: #or conex not frontier:
                pq.add((conex,cost_n+cost))
            


def main():
    
    max_height = int(input())
    start_structure = str(input())
    goal_structure = str(input())
    start_structure = start_structure.strip().split(";")
    goal_structure = goal_structure.strip().split(";")
    start_structure = list(map(lambda x: x.strip().strip("(").strip(")"), start_structure))
    goal_structure = list(map(lambda x: x.strip().strip("(").strip(")"), goal_structure))
    start_structure = list(map(lambda x: x.split(", ") if x != '' else [], start_structure))
    goal_structure = list(map(lambda x: x.split(", ") if x != '' else [], goal_structure))
    print('G?->',goal_structure)
    print('S?->',start_structure)
    gsp=GraphSearchSpace()
    initialState = Node(start_structure, max_height)
    initialState.generate_paths(gsp)
    

    #max_height = 2
    #goal_structure = [['A', 'C'], [], []]
    #start_structure = [['A'], ['B'], ['C']]
    gsp = GraphSearchSpace()
    initialState = Node(start_structure, max_height)
    goalState = Node(goal_structure, max_height)
    # a=set()
    # a.add(initialState)
    # second = Node(start_structure, max_height)
    # print(second in a)



    initialState.generate_paths(gsp)

    if goalState not in  gsp.nodes:
        print("Not Found GoalState")
    else:
        print("Found GoalState")

    ucs(initialState, goalState)
    #print("kmkm")
    #print(gsp.__str__())
    #for i in initialState.conections:
        #print(i)

'''

[x] S. Russell and P. Norvig, Artificial intelligence, 3rd ed. 2010: Pearson Education,Inc., 2010.
function UNIFORM-COST-SEARCH(problem) returns a solution, or failure
    node ← a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
    frontier ← a priority queue ordered by PATH-COST, with node as the only element explored ← an empty set
    loop do
    if EMPTY?(frontier) then return failure
    node←POP(frontier) /*choosesthelowest-costnodeinfrontier */
    if problem.GOAL-TEST(node.STATE) then return SOLUTION(node) add node.STATE to explored
    for each action in problem.ACTIONS(node.STATE) do
        child ←CHILD-NODE(problem,node,action)
        if child.STATE is not in explored or frontier then
            frontier ←INSERT(child,frontier)
        else if child.STATE is in frontier with higher PATH-COST then
            replace that frontier node with child

'''

class PriorityQueue():

    def is_empty(self):
        if len(self.q)==0:
            return True
        return False

    def __init__(self):
        self.q=deque([])

    def __str__(self):
        s="\n-----------\n"
        for i in self.q:
            s=s+str(i[0])+", "+str(i[1])+";\n"
        return s


    def pop(self):
        self.q=deque(self.q)
        return self.q.popleft()
    
    def add(self, paired):
        self.q.append(paired)
        self.q=sorted(self.q, key= lambda x : x[1])

    


if __name__ == "__main__":
    main()
    # pq=PriorityQueue()
    # pq.add((22, 3))
    # pq.add((27, 100))
    # pq.add((1,2 ))
    # print(str(pq))
    # pq.add((45, 2))
    # pq.add((2,3))
    # print(str(pq))
    # pq.pop()
    # pq.pop()
    # print(str(pq))







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
