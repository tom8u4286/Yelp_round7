


f = open("../data/line-data/cooccurrence/restaurant_1_cooccur.txt")

word_list = []

for line in f:
    lst = line.split(" ")
    if lst[0] not in word_list:
        word_list.append(lst[0])
    if lst[1] not in word_list:
        word_list.append(lst[1])

print len(word_list)
