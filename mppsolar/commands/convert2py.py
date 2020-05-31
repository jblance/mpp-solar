import json
from glob import glob

file_names = glob('./*.json')

out_dict = {}

for file_name in file_names:
    with open(file_name, 'r') as f:
        file_data = json.loads(f.read())
        name = file_data['name']
        out_dict[name] = file_data

with open('../all_commands.py', 'w') as out_file:
    json.dump(out_dict, out_file, sort_keys=True, indent=4)

