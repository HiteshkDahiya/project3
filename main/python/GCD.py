a = 18
b = 24
def find_gcd(a,b):
    for i in range(a,1,-1):
        for j in range(b,1,-1):
            if i == j and a%i == 0 and b%j == 0:
                return i

gcd = find_gcd(a,b)
print(gcd)