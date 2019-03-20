from collections import deque

def total_probalility(calculated_values, variables, query):
	''' P(B) = P(B|A1)*P(A1) + P(B|A2)*P(A2) + ... + P(B|An)*P(An) '''

	aux= query[1:]
	total=0
	
	for p in variables:
		if p != aux:
			positive, calculated_values = find_probability(query+'|'+'+'+p, calculated_values, variables)
			calculated_values[query+'|'+'+'+p]= positive

			negative, calculated_values = find_probability(query+'|'+'-'+p, calculated_values, variables)
			calculated_values[query+'|'+'-'+p]= negative

			positive_multiplicator, calculated_values = find_probability('+'+p, calculated_values, variables)
			calculated_values['+'+p]=positive_multiplicator

			negative_multiplicator, calculated_values = find_probability('-'+p, calculated_values, variables)
			calculated_values['-'+p]=negative_multiplicator

			total = total + (positive*positive_multiplicator)
			total = total + (negative*negative_multiplicator)
	
	calculated_values[query]=total
	return total, calculated_values


			




def bayes_therorem(calculated_values, variables, query):
	''' P(A|B) = (P(B|A) * P(A)) / P(B) '''
	subqueries = query.split("|")
	
	first_numerator_query= "|".join(reversed(subqueries))
	if first_numerator_query in calculated_values:
		first_numerator, calculated_values= find_probability(first_numerator_query, calculated_values, variables)
		calculated_values[first_numerator_query]=first_numerator
		second_numerator_query=subqueries[0]
		second_numerator, calculated_values = find_probability(second_numerator_query, calculated_values, variables)
		calculated_values[second_numerator_query]=second_numerator
		

		denominator_query = subqueries[-1]
		denominator, calculated_values = find_probability(denominator_query, calculated_values, variables)
		calculated_values[denominator_query]= denominator

		bayes = (first_numerator*second_numerator) / denominator
		calculated_values[query]=bayes

		return bayes, calculated_values

	else:
		# P(A|B) = chainrule(a,b) / P(B)
		# P(A|B) = chainrule(b,a) / P(B)
		# P(query)
		# conditional probability with chain rulE
		# +Burglary|+Earthquake,+JohnCalls =  Chain(+Burglary,+Earthquake,+JohnCalls) / chain(+Earthquake,+JohnCalls )
		print("->", query)
		merged_for_chain = ",".join(subqueries)
		chain_rule(merged_for_chain, calculated_values, variables)
		return -1, calculated_values

	

def chain_rule(query_list, calculated_values, variables):
	elements_listed= set([x.strip() for x in query_list.split(",")])
	keys_in_general_set= set(calculated_values.keys())
	existence = elements_listed&keys_in_general_set

	queue = deque([])
	t=1
	if (len(existence)>0):
		queue.append(existence.pop())
	else:
		#calc 4 pass
		pass


	counter = 1
	while(elements_listed):
		q = queue.popleft()
		elements_listed.remove(q)
		multiplicator, calculated_values = find_probability(q, calculated_values, variables)
		calculated_values[q]=multiplicator
		e=elements_listed.pop()
		other_value, calculated_values = find_probability( e+'|'+q  , calculated_values, variables)
		el = [q,e]
		calculated_values[",".join(sorted(el))] = other_value

		


		

	
def find_probability(query, calculated_values, variables):

	if query in calculated_values:
		return calculated_values[query] , calculated_values
	else:

		negative_variable = '-'+query[1:]
		positive_variable = '+'+query[1:]

		# Find the negative compliment if the positive exists
		if (query.startswith('+') and negative_variable in calculated_values):
			calculated_complement = 1 - calculated_values[negative_variable]
			calculated_values[positive_variable]=calculated_complement
			return calculated_complement, calculated_values
		
		# Find the positive compliment if the negative exists
		elif (query.startswith('-') and positive_variable in calculated_values):
			calculated_complement = 1 - calculated_values[positive_variable]
			calculated_values[negative_variable]=calculated_complement
			return calculated_complement, calculated_values

		else:

			
			if query.find('|') == -1 and query.find(',') == -1:
				total, calculated_values = total_probalility(calculated_values, variables, query)
				return total, calculated_values 

			else:
				bayes, calculated_values = bayes_therorem(calculated_values, variables, query)
				return bayes, calculated_values


	

def main():
	# Parsing input

	# variables = str(input())
	# variables = variables.split(",")
	# variables = set([x.strip() for x in variables])
	# amount_of_values = int(input())

	# calculated_values = {}
	# for i in range(amount_of_values):
	# 	value_string = str(input())
	# 	value_string = [x.strip() for x in value_string.split("=")]
	# 	calculated_values[str(value_string[0])]=float(value_string[1])
	
	
	# amount_of_queries = int(input())
	# queries = []
	# for i in range(amount_of_queries):
	# 	queries.append(str(input()))

	# print(calculated_values)
	# print('Q:',queries)
	# print(variables)

	# calculated_values = {'+Ill': 0.001, '+Test|+Ill': 0.9, '+Test|-Ill': 0.5}
	# queries = ['+Ill', '-Ill', '+Ill|+Test', '+Test', '-Test', '+Test|+Ill', '+Test|-Ill']
	# variables ={'Test', 'Ill'}

	calculated_values = {'+Burglary': 0.001, '+Earthquake': 0.002, '+Alarm|+Earthquake,+Burglary': 0.95, '+Alarm|-Earthquake,+Burglary': 0.94, '+Alarm|+Earthquake,-Burglary': 0.29, '+Alarm|-Earthquake,-Burglary': 0.001, '+JohnCalls|+Alarm': 0.9, '+JohnCalls|-Alarm': 0.05, '+MaryCalls|+Alarm': 0.7, '+MaryCalls|-Alarm': 0.01}
	queries = ['+Burglary|+Earthquake,+JohnCalls', '+Earthquake', '-MaryCalls|+Earthquake,+Alarm', '+JohnCalls|-Earthquake,-MaryCalls,+Burglary', '-Alarm|-Earthquake,-MaryCalls,+Burglary', '-Alarm,+JohnCalls|-Earthquake,-MaryCalls,+Burglary']
	variables = {'Alarm', 'Burglary', 'JohnCalls', 'MaryCalls', 'Earthquake'}
    
	answers=[]
	for query in queries:
		answer, calculated_values = find_probability(query, calculated_values, variables)
		answers.append(answer)


	print("\n".join([str(x) for x in answers]))


	# print (calculated_values)









if __name__ == "__main__":
	main()
	



