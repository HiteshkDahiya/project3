import random
n = int(input('Enter a integer Number:'))
list = []
for i in range(n):
    list.append(i+1)

a = random.randint(1,n+1)
list.remove(a)
for i in range(n):
    if i+1 not in list:
        print(i+1,'is the number that missing from list')