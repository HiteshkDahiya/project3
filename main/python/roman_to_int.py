def roman_to_int(s):
    roman_map = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
    int = 0
    pre_val = 0
    for a in reversed(s):
        val = roman_map[a]
        if val < pre_val:
            int -= val
        else:
            int += val
            pre_val = val
    return int

print(roman_to_int('III'))
print(roman_to_int('V'))
print(roman_to_int('IV'))
print(roman_to_int('VI'))
print(roman_to_int('XXX'))