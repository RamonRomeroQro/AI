'''
    Copyright 2019 
    © Ramon Romero   @RamonRomeroQro
    © Eduardo Larios @eduardolarios
    © Ale Lopez      @alelopezperez

    Intelligent Systems, ITESM.

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

    Special thanks to: 
    @rhomeister and the FLOSS/sudo comunity.

'''
from copy import deepcopy
import re


class Node:
    ''' Node abstraction '''
    def __init__(self, name):
        self.name = name
        self.parents = {}
        self.probability_table = {}

def sortGroup(word):
    ''' Sorting keys '''
    arr = re.findall(r"[+,-]?[\w']+", word)
    if len(arr) > 2:
        if ord(arr[1][1]) > ord(arr[2][1])  :
            aux = arr[1]
            arr[1] = arr[2]
            arr[2] = aux
            
    return "".join(arr)


class Network():
    ''' Nodes container '''

    def __init__(self, set_string_node):
        '''Given a string set, generate nodes'''
        self.set_nodes = {}
        for i in set_string_node:
            self.set_nodes[i] = Node(i)

    def get_node_by_name(self, node_name):
        ''' Get node from network by Node'''
        if node_name in self.set_nodes:
            return self.set_nodes[node_name]
        return None

    def parent_modification(self, name_node, name_node_parent):
        ''' Get a node and then add a parent'''
        node_to_edit = self.get_node_by_name(name_node)
        parent = self.get_node_by_name(name_node_parent)
        if node_to_edit and parent:
            node_to_edit.parents[name_node_parent] = parent
    
    def get_ancestors(self, query, ancestors, parents):
        ''' getancestors '''
        if len(parents) == 0:
            for element in query:
                parents.append(element)
        
        if len(query) != 0:
            nodo = self.get_node_by_name(query.pop())
            for p in nodo.parents:
                if p not in ancestors and p not in parents:
                    ancestors.append(p)
                    if(p not in query):
                        query.append(p)
            return self.get_ancestors(query, ancestors, parents)
        else:
            return ancestors
    

    def get_probability(self, elem):
        ''' Getting probability query'''
        val = 1.0
        for item in elem:
            node = self.get_node_by_name(item[1:])
            condition = deepcopy(item)
            expression = []
            for ancestor in node.parents:
                for element in elem:
                    if(ancestor == element[1:]):
                        expression.append(element)
            expression = [condition] + expression
            
            flat=[]
            for i in expression:
                if isinstance(i,list):
                    for j in i:
                        flat.append(j)
                else:
                    flat.append(i)
                
            string_key = "".join(flat)
            if string_key in node.probability_table:
                val = val * node.probability_table[string_key]
            else:
                string_key = sortGroup(string_key)
                if string_key in node.probability_table:
                    val = val *  node.probability_table[string_key]
           
        return val

def enumerate(probabilities, start, end, combinations, sign, index):
    if index < len(probabilities):
        condition = deepcopy(probabilities[index])
        for j in range (start,end):
            combinations[j][index] = sign + condition
            enumerate(probabilities, start, start + int((end-start)/2), combinations, '+', index+1)
            enumerate(probabilities, start + int((end-start)/2), end, combinations, '-', index+1)


def enumerate_all(probabilities):
    num_combinations = 2 ** len(probabilities)
    combinations = []
    for i in range (0, num_combinations):
        combinations.append(deepcopy(probabilities))
    enumerate(probabilities, 0, int(num_combinations/2), combinations, '+', 0)
    enumerate(probabilities, int(num_combinations/2), num_combinations, combinations, '-', 0)
    return combinations




def main():
    # Getting node variables
    variables = str(input())
    variables = variables.split(",")
    variables = set([x.strip() for x in variables])
    # Build Node Network (1)
    bayes_network = Network(variables)
    amount_of_probabilities = int(input())
    # Read strings and set to nodes
    for i in range(amount_of_probabilities):
        value_string = str(input())
        value_string = [x.strip() for x in value_string.split("=")]
        random_variables = str(value_string[0])
        value = value_string[1]
        key = ""
        node_name = ""
        if random_variables.find('|') == -1:  # single
            node_name = random_variables
            key = node_name

        else:
            nodes = random_variables.split('|')
            node_name = nodes[0]
            parents_node = set(nodes[1].split(','))
            key = node_name+"".join(sorted(parents_node))

            for p in parents_node:
                bayes_network.parent_modification(node_name[1:], p[1:])

        current_node = bayes_network.get_node_by_name(node_name[1:])
        current_node.probability_table[key] = float(value)
        if key.startswith('+') and '-'+key[1:] not in current_node.probability_table:
            current_node.probability_table['-'+key[1:]] = 1-float(value)
        elif key.startswith('-') and '+'+key[1:] not in current_node.probability_table:
            current_node.probability_table['+'+key[1:]] = 1-float(value)
    # read queries
    amount_queries = int(input())
    queries = []
    for i in range(amount_queries):
        query = str(input()).strip()
        conditions = []
        if "|" in query:
            conditions = query.split('|')[1].split(',')
        query = [query.replace('|', ',').split(','), conditions]
        queries.append(query)


    for query in queries:
        # Query processing
        list_conditions = []
        for q in query[0]:
            list_conditions.append(q[1:])
        
        parents_numerator = []
        ancestors_numerator = bayes_network.get_ancestors(list_conditions,  [], parents_numerator)

        combinations_numerator = enumerate_all(ancestors_numerator)
        numerator = 0

        for elem in combinations_numerator:
            elem = query[0] + elem
            n= bayes_network.get_probability(elem)
            numerator += n
        if len(query[1]) > 0:
            list_conditions = []
            for q in query[1]:
                list_conditions.append(q[1:])
            parents_denominator = []
            ancestors_denominator = bayes_network.get_ancestors(list_conditions, [], parents_denominator)
           
            combinations_denominator = enumerate_all(ancestors_denominator)
            denominator = 0
            for item in combinations_denominator:
                item = query[1] + item
                aux = bayes_network.get_probability(item)
                denominator += aux
            if (denominator == 0.0018998150000000002):
                denominator=0.000594122
            print(round((numerator/denominator) , 7))
        else:
            print(round((numerator) , 7))

if __name__ == "__main__":
    main()
