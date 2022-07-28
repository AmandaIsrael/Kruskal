dicio = {
    
}

if not '0' in dicio:
    dicio['0'] = []
dicio['0'].append("huhuhu")

keys = [int(key) for key in dicio.keys()]
keys.sort()
print(keys)

for key in keys:
    l = dicio[str(key)]
    for ele in l:
        print(ele)