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
    
# Here is DL to LD:

# v = [dict(zip(DL,t)) for t in zip(*DL.values())]
# print(v)

# and LD to DL:

# v = {k: [dic[k] for dic in LD] for k in LD[0]}
# print(v)

    def subset(self, key, value):
        new_listed_info=[]
        for element in self.listed_info:
            if key in element and element[key]==value:
                new_listed_info.append(element)

        new_info = defaultdict(list)
        if key in self.info:
            for e in self.info[key]:
                if e == value:
                    new_info[key].append(e)
        

        ndts= DataSet()
        ndts.relationship_name=self.relationship_name
        ndts.attributes=self.attributes
        ndts.info=new_info
        ndts.listed_info=new_listed_info
        return ndts

     
if __name__ == "__main__":
    data_set=DataSet()
    data_set.update_from_input()
    f = open("qk.csv", "w+")
    f.write(",".join(data_set.list_attributes)+"\n")
    f.write("\n".join([",".join([v for v in i.values()]) for i in data_set.listed_info]))
    f.close()