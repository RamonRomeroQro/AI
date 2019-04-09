'''
    Copyright 2019 
    © Ramon Romero   @RamonRomeroQro

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
    Ruben Stranders @rhomeister and the FLOSS/SUDO comunity.
    Python 3.7.2 (PEP8)

'''
from collections import defaultdict, Counter
import copy
import math


class DataSet():
    ''' Data set class abstractiion'''

    def __init__(self):
        ''' Base constructor '''
        self.relationship_name = ""
        self.attributes = {}
        self.list_attributes = []
        self.info = defaultdict(list)  # arr row
        self.listed_info = []  # arr dic

    def change_from_listed(self, list_i):
        ''' change data set contents given list '''
        self.listed_info = list_i
        self.info = {k: [dic[k] for dic in self.listed_info]
                     for k in self.listed_info[0]}

        # Here is DL to LD:
        # v = [dict(zip(DL,t)) for t in zip(*DL.values())]
        # print(v)

        # and LD to DL:
        # v = {k: [dic[k] for dic in LD] for k in LD[0]}
        # print(v)

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
                        read_line = read_line.split(" ")
                        self.relationship_name = read_line[1]
                    elif read_line.startswith("@attribute"):
                        read_line = read_line.split()
                        attribute_name = read_line[1]
                        self.list_attributes.append(attribute_name)
                        unparsed_possibilities = read_line[2:]
                        unparsed_possibilities = "".join(unparsed_possibilities)
                        unparsed_possibilities = unparsed_possibilities.strip('{').strip('}').split(',')
                        self.attributes[attribute_name] = unparsed_possibilities
                    elif read_line.startswith("@data"):
                        while(1):
                            try:
                                read_data = str(input()).strip()
                                if read_data.startswith('@'):
                                    pass
                                elif read_data.startswith('%'):
                                    pass
                                else:
                                    read_data = [e.strip()
                                                 for e in read_data.split(",")]
                                    listed_element = {}
                                    for i in range(len(self.list_attributes)):
                                        self.info[self.list_attributes[i]].append(
                                            read_data[i])
                                        listed_element[self.list_attributes[i]
                                                       ] = read_data[i]
                                    self.listed_info.append(listed_element)

                            except EOFError:
                                break
            except EOFError:
                break


def calc_entropy_desition(data_set):
    '''calcular entropia de desicion dado un dataset'''
    last_key = data_set.list_attributes[-1]
    arr = data_set.info[last_key]
    counter1 = Counter(arr)
    entropy = 0
    for v in counter1.values():
        entropy = entropy + ((v/len(arr)) * math.log2((v/len(arr))))
    return entropy*-1


def all_same_desition(data_set):
    ''' contador ultima columna '''
    last_key = data_set.list_attributes[-1]
    counter1 = Counter(data_set.info[last_key])
    return counter1

def split_by_key(data_set, key):
    ''' information gain by key '''
    desition_key = data_set.list_attributes[-1]
    elements_splited_by_key = defaultdict(list)
    for element in data_set.listed_info:
        if element[key] not in elements_splited_by_key:
            elements_splited_by_key[element[key]].append(element)
        else:
            elements_splited_by_key[element[key]].append(element)

    counter_by_cat = {}  # contador de elementos dentro de columna
    for k, v in elements_splited_by_key.items():
        counter_by_cat[k] = len(v)

    counter_cat_desition = {}
    elements_key_desition = {}
    for k, l in elements_splited_by_key.items():
        elements_key_desition[k] = defaultdict(list)
        for i in l:
            if i[desition_key] not in elements_key_desition[k]:
                elements_key_desition[k][i[desition_key]].append(i)
            else:
                elements_key_desition[k][i[desition_key]].append(i)

    counter_cat_desition = {}
    for k, v in elements_key_desition.items():
        counter_cat_desition[k] = {}
        for e in v:
            counter_cat_desition[k][e] = len(elements_key_desition[k][e])
    entropies = {}
    for k, v in counter_cat_desition.items():
        middle_entropy = 0

        for i in v:
            middle_entropy = middle_entropy + (((counter_cat_desition[k][i])/(
                counter_by_cat[k]))*math.log(((counter_cat_desition[k][i])/(counter_by_cat[k]))))
        entropies[k] = (middle_entropy*-1)
        # Married = LLLLM = -1*((4/5 log2(4/5))+(1/5 log2(1/5))) = .72
        # Single = LMMHH = -1*((1/5 log2(1/5))+(2/5 log2(2/5)) + (2/5 log2(2/5))) = 1.52

    size_set = sum([v for v in counter_by_cat.values()])

    return counter_by_cat, entropies, size_set


def splitter(data_set, key):
    ''' generate subset by key '''
    splitted = defaultdict(list)
    for e in data_set.listed_info:
        if e[key] not in splitted:
            splitted[e[key]].append(e)
        else:
            splitted[e[key]].append(e)
    arrdata = {}
    updated_list = copy.deepcopy(data_set.list_attributes)
    updated_list.remove(key)

    for k, v in splitted.items():
        new_data_set = DataSet()
        new_data_set.change_from_listed(v)  # info and listed info
        new_data_set.relationship_name = data_set.relationship_name
        new_data_set.list_attributes = updated_list
        for col in new_data_set.list_attributes:
            new_data_set.attributes[col] = data_set.attributes[col]
        arrdata[k] = (new_data_set)

    return arrdata


def generate_tree(data_set, deepth):
    ''' generate tree '''
    counter = all_same_desition(data_set)
    if len(counter) == 1:
        for k in counter.keys():
            print((" "*(deepth+1))+"ANSWER: "+k)
        return
    else:
        current_entropy = calc_entropy_desition(data_set)
        max_gain = -100
        node = ""
        for columna in data_set.list_attributes[:-1]:
            counter_cat, entropies, size_set = split_by_key(data_set, columna)
            sub = 0
            for k, v in counter_cat.items():
                sub = sub+((v/size_set)*entropies[k])
            infogain = current_entropy-sub
            if infogain > max_gain:
                max_gain = infogain
                node = columna

        arr_data = splitter(data_set, node)
        for i in data_set.attributes[node]:
            for k, v in arr_data.items():
                if k==i:
                    print(((" "*deepth)+node+": "+str(k)))
                    generate_tree(v, deepth+1)


def main():
    data_set = DataSet()
    data_set.update_from_input()
    generate_tree(data_set, 0)


if __name__ == "__main__":
    main()
