from collections import deque

class GraphSearchSpace():
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def add_conection(self, node1, node2, o_stack, dest_stack):
        #print(1,node1.__str__())
        self.nodes.add(node1)
        #print(2,node2.__str__())
        self.nodes.add(node2)


        n1_to_n2=Edge(node1, node2, o_stack, dest_stack)
        n2_to_n1=Edge(node1, node2, dest_stack, o_stack)
        self.edges.add(n1_to_n2)
        self.edges.add(n2_to_n1)

    def __str__(self):
        # s=""
        # for i in self.nodes:
        #     s=s+i.__str__()+"\n"
        # return s
        s=""
        for i in self.edges:
            s=s+i.__str__()+"\n"

        return s


   
            



class Edge():
    def __str__(self):
        return (self.origin.__str__()+"\t $: "+str(self.cost)+" Or: "+str(self.o_s)+" De: "+str(self.d_s)+" \t"+self.destination.__str__())

    def __init__(self, node1, node2, o_stack, dest_stack):
        self.origin= node1
        self.destination=node2
        self.o_s=o_stack
        self.d_s=dest_stack
        # Example: moving a container from stack 2 to stack 4 takes 0.5 + abs(2 - 4) + 0.5 = 3 minutes.
        self.cost=1+abs(o_stack-dest_stack)

    def __eq__(self, other):
        return isinstance(other, Edge) and self.destination == other.destination and self.origin == other.origin
    
    def __hash__(self):
        # use the hashcode of self.ssn since that is used
        # for equality checks as well
        return hash(self.origin.hashing_str+self.destination.hashing_str+ str(self.cost))
        

class Node:
    def __str__(self):
        return self.structure.__str__()

    def __eq__(self, other):
        return isinstance(other, Node) and self.structure == other.structure
    
    def __hash__(self):
        # use the hashcode of self.ssn since that is used
        # for equality checks as well
        
        #return hash((self.hashing_str, self.num_stacks, self.max_height))
        return hash()


    def __init__(self, structure, h):
        self.num_stacks = len(structure)
        self.max_height = h
        self.structure = structure


        s=""
        for i in self.structure:
            if len(i)==0:
                s=s+"[X]"
            else:
                s=s+"["+",".join(i)+"]"

        self.hashing_str=s



    def generate_paths(self, gsp):
        # q=deque([i for i in range(0,self.num_stacks)])
        # for i in range(0,self.num_stacks):
        #     e=q.popleft()
        #     q.append(e)
        #     for j in range(1+i,len(q)):
        #         #print(i,j)
        #         self.transition_model(i,j,gsp)
        #         self.transition_model(j,i,gsp)
        for i in range(0,self.num_stacks):
            for j in range(0,self.num_stacks):
                
                if i!=j:
                    self.transition_model(i,j,gsp)




    
    def transition_model(self, origin_stack, destination_stack, gsp):
        if len(self.structure[destination_stack])+1<=self.max_height and (len(self.structure[origin_stack])-1)>=0:
            new_structure = list(map(list, self.structure))
            e = new_structure[origin_stack].pop()
            new_structure[destination_stack].append(e)
            new_node=Node(new_structure, self.max_height)

            if origin_stack==1 and destination_stack==2 and self.structure==([['A'], ['B'], ['C']]):
                    #print(self, 'ddd', new_node, [ x.structure for x in gsp.nodes ])
                    print(new_node not in gsp.nodes, new_node.structure)
            if new_node not in gsp.nodes:
                #print("!",new_structure, self.structure)
                gsp.add_conection(self, new_node, origin_stack, destination_stack)
                new_node.generate_paths(gsp)

        







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
    goal_structure= [['A', 'C'], [], []]
    start_structure = [['A'], ['B'], ['C']]
    
    gsp=GraphSearchSpace()

    initialState = Node(start_structure, max_height)
    initialState.generate_paths(gsp)

    #print(gsp.__str__())


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