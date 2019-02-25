#import fileinput

#lines = []
# for line in fileinput.input():
#    lines.append(line.strip())
# num=list(map(int,lines[0]))[0]
# print(sum(num))

a = int(input())
start = str(input())
goal = str(input())
start = start.strip().split(";")
goal = goal.strip().split(";")
start = list(map(lambda x: x.strip().strip("(").strip(")"), start))
goal = list(map(lambda x: x.strip().strip("(").strip(")"), goal))
start = list(map(lambda x: x.split(", ") if x != "X" else [], start))
goal = list(map(lambda x: x.split(", ") if x != "X" else [], goal))
print(start)
print(goal)
