dt = {'1':1,'2':2,'3':{'3a':3},'4':{'4a':4,'5':{'5a':5,'6':6}}}

def flatten_dict(dt, parent_key=''):
    flat = {}
    for key, value in dt.items():
        new_key = f'{ parent_key }.{ key }' if parent_key else key
        if isinstance(value, dict):
            flat.update(flatten_dict(value, parent_key=new_key))
        else:
            flat.update({new_key:value})

    return flat

print(flatten_dict(dt))