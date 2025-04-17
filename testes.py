import json
data = {}
with open("credentials(exemplo).json", 'r') as file:
    data = json.load(file)

file.close()

print(data, type(data))

print(list(data))
    