import sys
from copy import deepcopy

def get_ancestors(query, table, ancestors, parents):
    if len(parents) == 0:
        for element in query:
            parents.append(element)
    if len(query) != 0:
        for ancestor in table[query[0]]['ancestors']:
            if ancestor not in ancestors and ancestor not in parents:
                ancestors.append(ancestor)
                if(ancestor not in query):
                    query.append(ancestor)
        return get_ancestors(query[1:], table, ancestors, parents)
    else:
        return ancestors

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


def get_probability(table, elem):
    val = 1.0
    for item in elem:
        node = table[item[1:]]
        condition = deepcopy(item)
        expression = []
        for ancestor in node['ancestors']:
            for element in elem:
                if(ancestor == element[1:]):
                    expression.append(element)
        expression = [condition] + expression
        for probability in node['probabilities']:
            if(probability[0:-1] == expression):
                val *= probability[-1]
    return val

# Read input
data = sys.stdin.readlines()
# Get nodes
nodes = data[0].rstrip("\n").split(",")
table = {}
# Create dictionary for all the probabilities and the ancestors
for i in range(0, len(nodes)):
    table[nodes[i]] = {'probabilities': [], 'ancestors': []}
# Get the probabilities from the given data
no_probabilities = int(data[1].rstrip("\n"))
probabilities = []
# Add the probabilities to the table
for i in range(2, no_probabilities + 2):
    probability = data[i].rstrip("\n").replace('|',',').replace('=',',').split(',')
    key = probability[0][1:]
    probability[len(probability) - 1] = float(probability[len(probability) - 1])
    table[key]['probabilities'].append(probability)
# Get queries
no_queries = int(data[no_probabilities + 2].rstrip("\n"))
queries = []
for i in range(no_probabilities + 3, no_queries + no_probabilities + 3):
    query = data[i].rstrip("\n")
    conditions = []
    if "|" in query:
        conditions = query.split('|')[1].split(',')
    query = [query.replace('|', ',').split(','), conditions]
    queries.append(query)
# Get all the probabilities and add them to the dictionary
for item in table:
    probabilities = table[item]['probabilities']
    for probability in probabilities:
        sign = probability[0][0]
        if(sign == '+'):
            new_sign = '-'
        else:
            new_sign = '+'
        new_probability = deepcopy(probability)
        new_probability[0] = new_sign + probability[0][1:]
        new_probability[len(new_probability) - 1] = round(1 - probability[len(new_probability) - 1], 7)
        if new_probability not in probabilities:
            probabilities.append(new_probability)
    # Get the ancestors of the nodes
    ancestors = table[item]['probabilities'][0][1:len(table[item]['probabilities'][0])-1]
    for i in range(0, len(ancestors)):
        ancestors[i] = ancestors[i][1:]
    table[item]['ancestors'] = ancestors
# Get result from the queries
for query in queries:
    # Get all the conditions from the query ex: Ill, Test
    list_conditions = []
    for q in query[0]:
        list_conditions.append(q[1:])
    parents_numerator = []
    ancestors_numerator = get_ancestors(list_conditions, table, [], parents_numerator)
    combinations_numerator = enumerate_all(ancestors_numerator)
    numerator = 0
    for elem in combinations_numerator:
        elem = query[0] + elem
        n= get_probability(table, elem)
        numerator += n
    if len(query[1]) > 0:
        list_conditions = []
        for q in query[1]:
            list_conditions.append(q[1:])
        parents_denominator = []
        ancestors_denominator = get_ancestors(list_conditions, table, [], parents_denominator)
        combinations_denominator = enumerate_all(ancestors_denominator)
        denominator = 0
        for item in combinations_denominator:
            item = query[1] + item
            aux = get_probability(table, item)
            denominator += aux
        print(round(numerator/denominator, 7))
    else:
        print(round(numerator,7))
