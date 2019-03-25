from collections import deque
import itertools

def total_probalility(probability_table, variables, query, bayes_network):
	''' P(B) = P(B|A1)*P(A1) + P(B|A2)*P(A2) + ... + P(B|An)*P(An) '''

	aux= query[1:]
	total=0
	
	for p in variables:
		if p != aux:
			positive, probability_table = find_probability(query+'|'+'+'+p, probability_table, variables, bayes_network)
			probability_table[query+'|'+'+'+p]= positive

			negative, probability_table = find_probability(query+'|'+'-'+p, probability_table, variables, bayes_network)
			probability_table[query+'|'+'-'+p]= negative

			positive_multiplicator, probability_table = find_probability('+'+p, probability_table, variables, bayes_network)
			probability_table['+'+p]=positive_multiplicator

			negative_multiplicator, probability_table = find_probability('-'+p, probability_table, variables, bayes_network)
			probability_table['-'+p]=negative_multiplicator

			total = total + (positive*positive_multiplicator)
			total = total + (negative*negative_multiplicator)
	
	probability_table[query]=total
	return total, probability_table


			




def bayes_therorem(probability_table, variables, query, bayes_network):
	''' P(A|B) = (P(B|A) * P(A)) / P(B) '''
	subqueries = query.split("|")
	first_numerator_query= "|".join(reversed(subqueries))
	if first_numerator_query in probability_table or '+'+first_numerator_query[1:] in probability_table or '-'+first_numerator_query[1:] in probability_table:
		first_numerator, probability_table= find_probability(first_numerator_query, probability_table, variables, bayes_network)
		probability_table[first_numerator_query]=first_numerator

		second_numerator_query=subqueries[0]
		second_numerator, probability_table = find_probability(second_numerator_query, probability_table, variables, bayes_network)
		probability_table[second_numerator_query]=second_numerator

		denominator_query = subqueries[-1]
		denominator, probability_table = find_probability(denominator_query, probability_table, variables, bayes_network)
		probability_table[denominator_query]= denominator

		bayes = (first_numerator*second_numerator) / denominator
		probability_table[query]=bayes
		return bayes, probability_table

	return conditional_probability(probability_table, variables, query, bayes_network)

	


def conditional_probability(probability_table, variables, query, bayes_network):
	print(query)
	new_query = query.split('|')
	numerator_elements = query.replace('|',',').split(',')
	numetator_nodes_keys= set([ x[1:] if x.startswith('+') or x.startswith('-')  else x for x in numerator_elements ])
	print('.N->' ,numerator_elements)
	print (numetator_nodes_keys)
	ancestors=set()
	for e in numetator_nodes_keys:
		new_ancestors = bayes_network.get_ancestors(e)
		ancestors = ancestors | new_ancestors
	node_names_pow2 = (numetator_nodes_keys-ancestors) | (ancestors-numetator_nodes_keys)
	
	r=0
	for ne in numerator_elements:
		print (ne)
		ok = ne[1:]
		nnode = bayes_network.get_node_by_name(ok)
		if nnode == None:
			bayes_network(ne[1:])
		if len(nnode.parents)==0:
			r=r*probability_table[ne]
		else:
			#los papas de que no sabesmos
			parents_eval = set(nnode.parents.keys())
			q=[]
			for k in parents_eval:
				for i in numerator_elements:
					if k in i:
						q.append(i)
			print(node_names_pow2)
			signs =  ['+', '-']
			product_hidden = list(itertools.product(signs, node_names_pow2))
			new_elements = [str(e[0])+str(e[1]) for e in product_hidden]
			for e in new_elements:
				find_probability(nnode.name+"|"+e)



	denominator_elements = new_query[1].split(',')
	print('.d->' ,denominator_elements)

	return -2, probability_table

def find_probability(query, probability_table, variables, bayes_network):

	if query in probability_table:
		return probability_table[query] , probability_table
	else:

		negative_variable = '-'+query[1:]
		positive_variable = '+'+query[1:]

		# Find the negative compliment if the positive exists
		if (query.startswith('+') and negative_variable in probability_table):
			calculated_complement = 1 - probability_table[negative_variable]
			probability_table[positive_variable]=calculated_complement
			return calculated_complement, probability_table
		
		# Find the positive compliment if the negative exists
		elif (query.startswith('-') and positive_variable in probability_table):
			calculated_complement = 1 - probability_table[positive_variable]
			probability_table[negative_variable]=calculated_complement
			return calculated_complement, probability_table

		else:

			if query.find('|') == -1:
				total, probability_table = total_probalility(probability_table, variables, query, bayes_network)
				return total, probability_table 

			else:
				bayes, probability_table = bayes_therorem(probability_table, variables, query, bayes_network)
				return bayes, probability_table




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

	def __str__(self):
		return "\n".join([ list(map(str, (k,v))) for k,v in self.set_nodes.items()])

			    
    
	def get_ancestors(self,node_name):
		"""Return set containing all vertices reachable from vertex."""
		node = self.get_node_by_name(node_name)
		visited = set()
		q = deque([])
		q.append(node.name)
		visited.add(node.name)
		while len(q)>0:
			current = self.get_node_by_name(q.popleft())
			for dest in current.parents.keys():
				if dest not in visited:
					visited.add(dest)
					q.append(self.get_node_by_name(dest).name)
		return visited



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
		if key.startswith('+') and '-'+key[1:] not in probability_table:
			probability_table['-'+key[1:]]=1-probability_table[key]
		if key.startswith('-') and '+'+key[1:] not in probability_table:
			probability_table['+'+key[1:]]=1-probability_table[key]

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

	for query in queries:
		answer, probability_table = find_probability(query, probability_table, variables, bayes_network)
		answers.append(answer)


	print("\n".join([str(x) for x in answers]))


	# print (probability_table)









if __name__ == "__main__":
	main()
	



