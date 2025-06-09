list = []
n = 10  # no. of elements in list
for i in range(n):
    list.append(i)

k = 4  # rotate the list by k positions
rotate_list = list[-k:] + list[:-k]
print(rotate_list)






# rotate_list = list.copy()
# for i in range(n-k):
#     rotate_list[k+i] = list[i]
#
# for i in range(k):
#     rotate_list[i] = list[n-k+i]
#
# print(rotate_list)



