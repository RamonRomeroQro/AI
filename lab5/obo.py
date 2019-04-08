import fileinput
import math
import pandas as pd
import numpy as np

relation = ""
attributes = {}


# Calculates the entropy
# dataframe= rows that should be taken into accoutn
def calculate_entropy(dataframe):
    occurrences = count_occurrences(dataframe)
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
def calculate_entropy_TX(dataframe, p):
    total_rows = dataframe.shape[0]
    result = 0
    filtered_rows = dataframe[p].value_counts().to_dict()
    for option in filtered_rows:
        # filter rows where equal to first possibility (p) and call calculate_entropy
        aux_entropy = calculate_entropy(dataframe[dataframe[p] == option])
        aux_row_count = dataframe[dataframe[p] == option].shape[0]
        result = result+(aux_row_count/total_rows*aux_entropy)
    # print("Entropy {0}: {1}".format(option, result))
    return result


# Calculates the information gain
#
def calculate_information_gain(dataframe, p, current_entropy):
    entropy_tx = calculate_entropy_TX(dataframe, p)
    return current_entropy - entropy_tx


# Stores in a dictionary how many times each value of the result occurs in the given part of the dataframe
# Output example {"yes":9, "no":4}
def count_occurrences(dataframe):
    y_column_name = list(attributes.keys())[-1]
    total_count = dataframe[y_column_name].value_counts().to_dict()
    return total_count


def format_header(header):
    name = header.replace("@attribute", "").split('{')[0].replace(" ", "")
    possible_values = header.replace("\n", "").replace("}", "").replace(" ", "").split('{')[1].split(',')
    # add to dictionary
    attributes[name] = possible_values


def format_data(data):
    matrix_data = []
    for i in range(0, len(data)):
        # add to row to matrix_data
        matrix_data.append(data[i].replace("\n", "").split(","))
    # transform matrix to numpy matrix
    np_matrix_data = np.matrix(matrix_data)
    # create dataframe from numpy matrix
    dataframe = pd.DataFrame(np_matrix_data)
    # add column names form the attributes dictionary
    dataframe.columns = attributes.keys()
    return dataframe


def same_y_values(dataframe):
    y_values = len(count_occurrences(dataframe))
    return y_values == 1


def generate_tree_model(dataframe, depth):
    # print("\n\n generate_tree_model() function call: \n data: ")
    # print(dataframe)
    tabulation = "  " * depth
    if same_y_values(dataframe):
        # print("all y values are the same, entropy is 0")
        y_column_name = list(attributes.keys())[-1]
        y_value = dataframe[y_column_name].iloc[0]
        print(tabulation + "ANSWER: {0}".format(y_value))
        return
    x_headers = list(dataframe.columns.values)[:-1]  # get x headers (ex. outlook temperature humidity  windy play)
    current_entropy = calculate_entropy(dataframe)

    max_information_gain = 0
    max_x_col = ""
    # calculate Information gain of each possible child
    for x_column in x_headers:
        information_gain = calculate_information_gain(dataframe, x_column, current_entropy)

        # select the column with the maximum information gain:
        if information_gain > max_information_gain:
            max_information_gain = information_gain
            max_x_col = x_column

    # print("split on column: {0}, information gain: {1}".format(max_x_col, max_information_gain))
    # for each attribute value, split dataframe:
    for value in attributes[max_x_col]:
        print(tabulation + "{0}: {1}".format(max_x_col, value))
        generate_tree_model(dataframe[dataframe[max_x_col] == value], depth + 1)
    return


def main():
    # example input
    file_input = fileinput.input()
    lines = []
    for x in file_input:
        if x[0] != '%':
            lines.append(x)

    input_len = len(lines)
    data_index = 0
    for i in range(0, input_len):
        header = lines[i].split(" ")[0]

        if "@attribute" in header:
                format_header(lines[i])
        elif "@data" in header:
            data_index = i
            break
    # print("attributes dictionary:")
    # print(attributes)
    dataframe = format_data(lines[data_index + 1:input_len])
    # print("\nfull dataframe:")

    generate_tree_model(dataframe, 0)


if __name__ == "__main__":
    main()