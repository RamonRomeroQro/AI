from collections import deque
import re
import copy
import sys
from decimal import Decimal
import itertools
from operator import itemgetter



class Node():
	def __init__(self, name):
		''' Creation by name Node '''
		self.name=name
		self.parents={}

class Network():
	''' Nodes container '''
	def __init__(self, set_string_node):
		'''Given a string set, generate nodes'''
		self.set_nodes={}
		for i in set_string_node:
			self.set_nodes[i]=Node(i)

	def getNode(self, node_name):
		''' Get node from network by Node'''
		if node_name in self.set_nodes:
			return self.set_nodes[node_name]
		return None
	
	def parent_modification(self, name_node, name_node_parent):
		''' Get a node and then add a parent'''
		node_to_edit = self.getNode(name_node)
		parent = self.getNode(name_node_parent)
		if node_to_edit and parent:
			node_to_edit.parents[name_node_parent]=parent

	def __str__(self):
		return "\n".join([ list(map(str, (k,v))) for k,v in self.set_nodes.items()])

			    
    
	def get_ancestors(self,node_name):
		"""Return set containing all vertices reachable from vertex."""
		node = self.getNode(node_name)
		visited = set()
		q = deque([])
		q.append(node.name)
		visited.add(node.name)
		while len(q)>0:
			current = self.getNode(q.popleft())
			for dest in current.parents.keys():
				if dest not in visited:
					visited.add(dest)
					q.append(self.getNode(dest).name)
		return visited

	def find_all_ancestors(self, node_queries):
		numetator_nodes_keys= set([ x[1:] if x.startswith('+') or x.startswith('-')  else x for x in node_queries ])
		ancestors=set()
		for e in numetator_nodes_keys:
			new_ancestors = self.get_ancestors(e)
			ancestors = ancestors | new_ancestors
		node_names_pow2 = (numetator_nodes_keys-ancestors) | (ancestors-numetator_nodes_keys)
		return ancestors, node_names_pow2
		
	
	




def main():
	# Getting node variables
	variables = str(input())
	variables = variables.split(",")
	variables = set([x.strip() for x in variables])

	# Build Node Network (1)
	bayes_network = Network(variables)

	# Get Probability table
	amount_of_probabilities = int(input())
	probability_table = {}

	for i in range(amount_of_probabilities):
		value_string = str(input())
		value_string = [x.strip() for x in value_string.split("=")]
		key = str(value_string[0])
		value = value_string[1]
		probability_table[key]=float(value)

		# checking substringing
		
		if key.find('|') != -1:
			broken_key = key.split("|")
			child_name = broken_key[0] 
			parents_names = broken_key[1].split(",")
			for p_name in parents_names:
				if p_name.startswith('+') or p_name.startswith('-'):
					p_name=p_name[1:]
				if child_name.startswith('+') or child_name.startswith('-'):
					child_name=child_name[1:]
				bayes_network.parent_modification(child_name,p_name)


	amount_of_queries = int(input())
	queries = []
	for i in range(amount_of_queries):
		queries.append(str(input()))

	# print(probability_table)
	# print(queries)
	# print(variables)

	# probability_table = {'+Ill': 0.001, '+Test|+Ill': 0.9, '+Test|-Ill': 0.5}
	# queries = ['+Ill', '-Ill', '+Ill|+Test', '+Test', '-Test', '+Test|+Ill', '+Test|-Ill']
	# variables ={'Test', 'Ill'}

	answers=[]

	# for query in queries:
	# 	answer, probability_table = find_probability(query, probability_table, variables, bayes_network)
	# 	answers.append(answer)

	processQueries(queries, bayes_network)
	print("\n".join([str(x) for x in answers]))


	# print (probability_table)





def processQueries(queries, bayes_network):
	ans=[]
	for q in queries:
		current = q.split('|')
		if (len(current) > 1):
			current = '|'.join(current)
			ans.append(conditional(current, bayes_network))
		else:
			current = str(current[0])
			ans.append(newComputeProbability(current, bayes_network))
	return "\n".join(ans)


def newComputeProbability(query, bayes_network):
    ##print("Thequery", query)
    query_array = query.split(',')
    #if intersection
    if(len(query_array) > 1 ):
        
        total_related_nodes, hidden = bayes_network.find_all_ancestors(query_array)
        signs =  ['+', '-']
        product_hidden = list(itertools.product(signs, hidden))
        product_hidden = sorted(product_hidden, key=itemgetter(1))
        #print("PRODUCT HIDDEN", product_hidden)
        if(len(product_hidden) >0 ):
            x = []
            product = []
            newqueries = []
            for i in range(len(product_hidden)):
              x.append(''.join(map(str, product_hidden[i])))

            for i in range(0, len(x), 2):
                product.append(x[i : i+2])

            query_string = ''.join(query_array)
            for t in itertools.product(*product):
                string =  query_string + t[0]
                string_arr = re.findall('[+|-][a-zA-Z0-9]*', string)
                newqueries.append(string_arr)

            for i in range(len(newqueries)):
                newqueries[i] = ','.join(newqueries[i])
            #print("QUERY CORRECTA", newqueries)
            cp = 0.0
            for q in newqueries:
                cp += chainRule(q, bayes_network)
            return(cp)
        else:

            for n in total_related_nodes:
                if (bayes_network.getNode(n) is not None):
                    pass
			
		    cp = chainRule(query, bayes_network)
			return(cp)
			
	else:
		query_probability = str(query_array[0])
		node_name = query_probability[1:0]
		node = bayes_network.getNode(node_name)
        #print("NODE NAME, NODE", node_name, node.__dict__)
        if(node.parents is None):
            #get direct probability from ptable
            sp = returnSingleProbability(node, query_probability)
            #print("ENTERED AND SHOULD RETURN", sp)
            return(sp)
        else:
            #total probability
            #si el nodo sí tiene padres entonces hacer total probability
            cp = totalProbability(query_probability)
            return(cp)


def chainRule(query):
    #print("----ENTERED CHAIN RULE with query----", query)
    result = 1.0
    query_array = query.split(',')
    #print("CHAIN RULE QUERY ARRAY", query_array)
    if(len(query_array) > 1):
        for q in query_array:
            node = net.find(stringWithoutSign(q))
            #print("NODE FOUND CHR", node.__dict__)
            if(node.parents is not None):
                #obtener de tabla de probabilidad
                for key, value in node.ptable.items():
                    #si cada elemento de la probabilidad del ptable, está contenido en el array del query
                    parents_array = re.findall('[+|-][a-zA-Z0-9]*', key)
                    difference_list = list(set(parents_array) - set(query_array))
                    #print("PARENTS ARRAY", parents_array, "QUERY ARRAY", query_array, "DIFFERENCE LIST", difference_list)
                    if(not difference_list):
                        result *= value
                        #print("Entré y ahora el resultado es", result)
                        break
                pass
            else:
                #return value
                sp = returnSingleProbability(node, q)
                result *= sp
                #print("Result chain rule", result)
        return result




def conditional(query, bayes_network):
    #print("+++++CONDITIONAL QUERY++++++", query)
    query = query.split('|')
    hypothesis = query[0]
    evidence = query[1]
    total = evidence + hypothesis
    upper = hypothesis + "," + evidence
    result = newComputeProbability(upper, bayes_network) / newComputeProbability(evidence, bayes_network)
    return result

if __name__ == "__main__":
	main()
	



