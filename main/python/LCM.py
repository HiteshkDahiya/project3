a = 18
b = 24
# flag = False
# for x in range(1,b+1):
#     for y in range(1,a+1):
#         if x * a == y * b:
#             print(f'{x*a} is LCM')
#             flag = True
#             break
#     if flag:
#         break

def find_lcm(a,b):
    for x in range(1,b+1):
        for y in range(1,a+1):
            if x * a == y * b:
                return x*a

print(find_lcm(a,b),f"is lcm of {a} and {b}")

