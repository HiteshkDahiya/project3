list1 = [1,2,3,4,[5,6],[7,[8,9]]]

def flatten_list(lst):
    flat = []
    for i in lst:
        if isinstance(i, list):
            flat.extend(flatten_list(i))
        else:
            flat.append(i)
    return flat

print(flatten_list(list1))
