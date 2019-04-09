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
    
   


    def select_where(self,key, desition_key):
        splits = defaultdict(list)
        for e in self.listed_info:
            if e[key] not in splits:
                splits[e[key]]=e
            else:
                splits[e[key]].append(e)

        partials={}
        for k,v in splits.items():
            counter, len1= counter_by_listdict(v,desition_key)
            s=0
            for v2 in counter.values():
                s=s+((v2/len(len1))* math.log2(v2/len(len1)))
            partials[k]=(s*-1)


        other, len2 = counter_by_listdict(self.info ,desition_key)
        s2=0
        for v3 in other.values():
            s2=s2+((v3/len(len2))* math.log2(v3/len(len2)))
        s2=(s2*-1)





def counter_by_listdict(listdict, key_to_count):
    c={}
    for i in listdict:
        if listdict[key_to_count] not in c:
            c[listdict[key_to_count]]=1
        else:
            c[listdict[key_to_count]]=c[listdict[key_to_count]]+1

    s= sum([v for v in c.values()])
    return c, s



def calc_entropy_desition(data_set):
    '''calcular entropia de desicion dado un dataset'''
    last_key=data_set.list_attributes[-1]
    arr=data_set.info[last_key]
    counter1= Counter(arr)
    entropy= 0
    for v in counter1.values(): 
        entropy= entropy + ((v/len(arr)) * math.log2((v/len(arr)))  )
    return entropy*-1

def all_same_desition(data_set):
    last_key=data_set.list_attributes[-1]
    counter1= Counter(data_set.info[last_key])
    return counter1

def split_by_key(data_set, key):
    desition_key=data_set.list_attributes[-1]
    elements_splited_by_key=defaultdict(list)
    for element in data_set.listed_info:
        if element[key] not in elements_splited_by_key:
            elements_splited_by_key[element[key]].append(element)
        else:
            elements_splited_by_key[element[key]].append(element)

    counter_by_cat={} # contador de elementos dentro de columna
    for k,v in elements_splited_by_key.items():
        counter_by_cat[k]=len(v)

    counter_cat_desition={}
    elements_key_desition={}
    for k,l in elements_splited_by_key.items():
        elements_key_desition[k]=defaultdict(list)
        for i in l:
            if i[desition_key] not in elements_key_desition[k]:
                elements_key_desition[k][i[desition_key]].append(i)
            else:
                elements_key_desition[k][i[desition_key]].append(i)

    counter_cat_desition={}
    for k,v in elements_key_desition.items():
        counter_cat_desition[k]={}
        for e in v:
            counter_cat_desition[k][e]=len(elements_key_desition[k][e])
    entropies={}
    for k,v  in counter_cat_desition.items():
        middle_entropy=0

        for i in v:
            middle_entropy=middle_entropy+ (((counter_cat_desition[k][i])/(counter_by_cat[k]))*math.log(((counter_cat_desition[k][i])/(counter_by_cat[k]))))
        entropies[k]=(middle_entropy*-1)
        # Married = LLLLM = -1*((4/5 log2(4/5))+(1/5 log2(1/5))) = .72
        # Single = LMMHH = -1*((1/5 log2(1/5))+(2/5 log2(2/5)) + (2/5 log2(2/5))) = 1.52

    size_set = sum([v for v in counter_by_cat.values()])

    return counter_by_cat, entropies, size_set


    



        

    


def generate_tree(data_set, deepth):
    counter = all_same_desition(data_set)
    if len(counter)==1:
        print ("all same retu")
        return
    else:
        current_entropy = calc_entropy_desition(data_set)
        max_gain=-100
        node=""
        for columna in data_set.list_attributes[:-1]:
            counter_cat, entropies, size_set = split_by_key( data_set, columna)
            sub=0
            for k,v in counter_cat.items():
                sub=sub+((v/size_set)*entropies[k])
            infogain=current_entropy-sub
            if infogain>max_gain:
                max_gain=infogain
                node=columna

        print('Root->', node)



            #1.48- (5/10 * .72 + 5/10*1.52) = .36

def main():
    data_set=DataSet()
    data_set.update_from_input()
    generate_tree(data_set, 0)
   

if __name__ == "__main__":
    main()