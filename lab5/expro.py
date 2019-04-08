from collections import defaultdict, Counter
from copy import deepcopy
import math

class DataSet():
    ''' Data set class abstractiion'''
    def __init__(self):
        self.relationship_name=""
        self.attributes={}
        self.list_attributes=[]
        self.info = defaultdict(list) # arr row
        self.listed_info = [] #arr dic
        
    def update_from_input(self):
        ''' Read from input '''
        while (1):
            try:
                read_line = str(input()).strip()
                if read_line == "":
                    pass
                elif read_line.startswith("%"):
                    pass
                else:
                    if read_line.startswith("@relation"):
                        read_line=read_line.split(" ")
                        self.relationship_name=read_line[1]
                    elif read_line.startswith("@attribute"):
                        read_line=read_line.split()
                        attribute_name=read_line[1]
                        self.list_attributes.append(attribute_name)
                        unparsed_possibilities=read_line[2:]
                        possibilities = [ x.strip('{').strip('}').strip(',') for x in unparsed_possibilities ]
                        self.attributes[attribute_name]= set(possibilities)
                    elif read_line.startswith("@data"):
                        while(1):
                            try:
                                read_data=str(input()).strip()
                                if read_data.startswith('@'):
                                    pass
                                elif read_data.startswith('%'):
                                    pass
                                else:
                                    read_data=[e.strip() for e in read_data.split(",")]
                                    listed_element={}
                                    for i in range(len(self.list_attributes)):
                                        self.info[self.list_attributes[i]].append(read_data[i])
                                        listed_element[self.list_attributes[i]]=read_data[i]
                                    self.listed_info.append(listed_element)
                                    
                            except EOFError:
                                break
            except EOFError:
                break

import pandas as pd

import fileinput
import math
import pandas as pd
import numpy as np

# Calculates the entropy
# dataframe= rows that should be taken into accoutn
def calculate_entropy(dataframe, data_set):
    occurrences = count_occurrences(dataframe, data_set)
    total_elements = dataframe.shape[0]
    result = 0
    for key in occurrences:
        elem_occurrences = occurrences[key]
        result = result - (elem_occurrences / total_elements * math.log2(elem_occurrences / total_elements))
    # print("Entropy: {0}".format(result))
    return result


# Calculates the entropy of the given possible child
# dataframe: full dataframe
# headers without including the outputs
def calculate_entropy_TX(dataframe, p, data_set):
    total_rows = dataframe.shape[0]
    result = 0
    filtered_rows = dataframe[p].value_counts().to_dict()
    for option in filtered_rows:
        # filter rows where equal to first possibility (p) and call calculate_entropy
        aux_entropy = calculate_entropy(dataframe[dataframe[p] == option], data_set)
        aux_row_count = dataframe[dataframe[p] == option].shape[0]
        result = result+(aux_row_count/total_rows*aux_entropy)
    # print("Entropy {0}: {1}".format(option, result))
    return result


# Calculates the information gain
#
def calculate_information_gain(dataframe, p, current_entropy, data_set):
    entropy_tx = calculate_entropy_TX(dataframe, p, data_set)
    return current_entropy - entropy_tx


# Stores in a dictionary how many times each value of the result occurs in the given part of the dataframe
# Output example {"yes":9, "no":4}
def count_occurrences(dataframe, data_set):
    y_column_name = list(data_set.attributes.keys())[-1]
    total_count = dataframe[y_column_name].value_counts().to_dict()
    return total_count


def same_y_values(dataframe, data_set):
    y_values = len(count_occurrences(dataframe, data_set))
    return y_values == 1


def generate_tree_model(dataframe, depth, data_set):
    tabulation = "  " * depth
    if same_y_values(dataframe, data_set):
        # print("all y values are the same, entropy is 0")
        y_column_name = list(data_set.attributes.keys())[-1]
        y_value = dataframe[y_column_name].iloc[0]
        print(tabulation + "ANSWER: {0}".format(y_value))
        return
    x_headers = list(dataframe.columns.values)[:-1]  # get x headers (ex. outlook temperature humidity  windy play)
    current_entropy = calculate_entropy(dataframe, data_set)

    max_information_gain = 0
    max_x_col = ""
    # calculate Information gain of each possible child
    for x_column in x_headers:
        information_gain = calculate_information_gain(dataframe, x_column, current_entropy, data_set)
        # select the column with the maximum information gain:
        if information_gain > max_information_gain:
            max_information_gain = information_gain
            max_x_col = x_column

    # print("split on column: {0}, information gain: {1}".format(max_x_col, max_information_gain))
    # for each attribute value, split dataframe:
    for value in data_set.attributes[max_x_col]:
        print(tabulation + "{0}: {1}".format(max_x_col, value))
        generate_tree_model(dataframe[dataframe[max_x_col] == value], depth + 1, data_set)
    return

def main():
    data_set=DataSet()
    data_set.update_from_input()
    f = open("qk.csv", "w+")
    f.write(",".join(data_set.list_attributes)+"\n")
    f.write("\n".join([",".join([v for v in i.values()]) for i in data_set.listed_info]))
    f.close()
    df=pd.read_csv("qk.csv", delimiter=',')
    # calc entropia del dataset
    generate_tree_model(df, 0, data_set)








if __name__ == "__main__":
    main()