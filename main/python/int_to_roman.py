def int_to_roman(n):
    val = [
        1000,900,500,400,
        100,90,50,40,
        10,9,5,4,
        1,
    ]
    syms = [
        'M','CM','D','DM',
        'C','XC','L','XL',
        'X','IX','V','IV',
        'I',
    ]
    roman = ''
    i = 0
    while n>0:
        count = n//val[i]
        roman += syms[i] * count
        n = n%val[i]
        i += 1

    return roman

print(int_to_roman(1123))