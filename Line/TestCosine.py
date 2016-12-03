import json
from scipy import spatial

f = open("../data/line-data/cosine_matrix/restaruant_1_cosine.json")
lst = json.loads(f.read())

print lst[3][2]

f2 = open("../data/line-data/vectors/200dim/restaurant_1_vector200.txt")
next(f2)
next(f2)
vec1 = [float(item) for item in next(f2).split(" ")[1:-1]]
vec2 = [float(item) for item in next(f2).split(" ")[1:-1]]

result = 1 - spatial.distance.cosine(vec1, vec2)

print result
