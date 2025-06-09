a = 90
b = 108

def find_lcm_gcd(a,b):
    def find_gcd(x,y):
        while y:
            x,y = y,x%y
        return x
    gcd = find_gcd(a,b)
    lcm = a*b//gcd
    return lcm,gcd

lcm,gcd = find_lcm_gcd(a,b)
print(lcm,gcd)