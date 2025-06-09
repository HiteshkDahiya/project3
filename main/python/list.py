str = 'Hello, What are doing?'
return_str = ''
count = 1
for x in str:
    if count%2 == 0:
        return_str += x.lower()
    else:
        return_str += x.upper()
    count += 1

print(return_str)

