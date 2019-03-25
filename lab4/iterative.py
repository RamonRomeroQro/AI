import re
import copy
import sys
from decimal import Decimal
import itertools
from operator import itemgetter



def totalProbability(query, bayes_network):
    node_name = query[1:]
    node = bayes_network.get_node_by_name(node_name)
    suma = 0.0
    for key, value in node.probability_table.items():
        if query in key:
            a = key.split(query)[1]
            a= re.findall('[+|-][a-zA-Z0-9]*', a)
            a = ','.join(a)
            #print("KEY", key, "A", a,  "QUERY", query)
            suma += compute_probability(a, bayes_network)*value
    return(suma)

def chainRule(query, bayes_network):
    result = 1.0
    query_array = query.split(',')
    if(len(query_array) > 1):
        for q in query_array:
            node = bayes_network.get_node_by_name(q[1:])
            if len(node.parents)!= 0:
                for key, value in node.probability_table.items():
                    parents_array = re.findall('[+|-][a-zA-Z0-9]*', key)
                    difference_list = list(set(parents_array) - set(query_array))
                    if(not difference_list):
                        result *= value
                        break
                pass
            else:
                sp = node.probability_table[q]
                result *= sp
        return result


class Node:
	''' Node abstraction '''
	def __init__(self, name):
		self.name = name
		self.parents = {}
		self.probability_table = {}

class Network():
	''' Nodes container '''
	def __init__(self, set_string_node):
		'''Given a string set, generate nodes'''
		self.set_nodes={}
		for i in set_string_node:
			self.set_nodes[i]=Node(i)

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
            node_to_edit.parents[name_node_parent]=parent
    
    def get_parents_from_list(self, nodes_with_sign):
        node_names= set([ x[1:] if x.startswith('+') or x.startswith('-')  else x for x in nodes_with_sign ])
        answer=set()
        print (node_name)
        for nn in node_names:
            node = self.get_node_by_name(nn)
            if len(node.parents)!=0:
                for k in node.parents.keys():
                    if k not in answer:
                        answer.add(k)
        return answer

def compute_probability(query, bayes_network):
	query_array = query.split(',')
	unsigned = []
	if(len(query_array) > 1 ):
		total_related_nodes = bayes_network.get_parents_from_list(query_array)
		unsigned_query_array = set(	[ x[1:] if x.startswith('+') or x.startswith('-')  else x for x in query_array ])
		intersection =  total_related_nodes - unsigned_query_array
		product_hidden = list(itertools.product(['+', '-'], intersection))
		product_hidden = sorted(product_hidden, key=itemgetter(1))
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
			cp = 0.0
			for q in newqueries:
				cp += chainRule(q, bayes_network)
			return(cp)
			###
		else:
			for n in total_related_nodes:
				node = bayes_network.get_node_by_name(n)
				if len(node.parents)!=0:
					pass
			cp = chainRule(query, bayes_network)
			return(cp)

	else:
		query_probability = str(query_array[0])
		node_name = query_probability[1:]
		node = bayes_network.get_node_by_name(node_name)
		if len(node.parents)==0:
			sp = node.probability_table[query_probability]
			
			return(sp)
		else:
			cp = totalProbability(query_probability, bayes_network)
			return(cp)



def conditional_probability(query, bayes_network):
	query = query.split('|')
	hypothesis = query[0]
	evidence = query[1]
	upper = ",".join(sorted([hypothesis, evidence]))
	result = compute_probability(upper, bayes_network) / compute_probability(evidence, bayes_network)
	return result

def main():
    # Getting node variables
	variables = str(input())
	variables = variables.split(",")
	variables = set([x.strip() for x in variables])

	# Build Node Network (1)
	bayes_network = Network(variables)

	amount_of_probabilities = int(input())

	for i in range(amount_of_probabilities):
		value_string = str(input())
		value_string = [x.strip() for x in value_string.split("=")]
		random_variables = str(value_string[0])
		value = value_string[1]
		key=""
		node_name=""
		if random_variables.find('|') == -1: # single
			node_name=random_variables
			key=node_name
			
		else:
			nodes = random_variables.split('|')
			node_name=nodes[0]
			parents_node=set(nodes[1].split(','))
			key=node_name+'|'+",".join(sorted(parents_node))

			for p in parents_node:
				bayes_network.parent_modification(node_name[1:], p[1:])

		current_node = bayes_network.get_node_by_name(node_name[1:])
		current_node.probability_table[key]=float(value)
		if key.startswith('+') and '-'+key[1:] not in current_node.probability_table:
			current_node.probability_table['-'+key[1:]]=1-float(value)
		elif key.startswith('-') and '+'+key[1:] not in current_node.probability_table:
			current_node.probability_table['+'+key[1:]]=1-float(value)
			
	amount_queries = int(input())
	queries = []
	for i in range(amount_queries):
		query= str(input()).strip()
		queries.append(query)

	print(evaluation(queries,bayes_network))


	

def evaluation(queries, bayes_network):
	answers = []
	for query in queries:
		prob=0.0
		if query.find("|") != -1:
			prob = conditional_probability(query, bayes_network)
		else:
			prob = compute_probability(query, bayes_network)
		print(prob)
		answers.append(prob)
	
	return answers




if __name__ == "__main__":
    main()