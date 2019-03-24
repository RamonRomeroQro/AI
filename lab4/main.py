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

def conditional_probability():
	pass

def chain_rule():
	pass

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

	for query in queries:
		answer, probability_table = find_probability(query, probability_table, variables, bayes_network)
		answers.append(answer)


	print("\n".join([str(x) for x in answers]))


	# print (probability_table)









if __name__ == "__main__":
	main()
	



