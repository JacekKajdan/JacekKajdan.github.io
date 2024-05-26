import json
import os
import random
import string

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_large_json(file_path, target_size_mb):
    data = []
    entry_size = 0
    count = 0

    while entry_size < target_size_mb * 1024 * 1024:
        entry = {
            "x": "100",
            "y": "100",
            "w": "100",
            "h": "100",
            "color": "#123abc"
        }
        data.append(entry)
        count += 1
        #entry_size = len(json.dumps(data))
        entry_size+=65
        print(entry_size)

    with open(file_path, 'w') as f:
        json.dump(data, f)

    print(f"Generated {file_path} with size: {os.path.getsize(file_path) / (1024 * 1024)} MB")

# Specify the file path and target size in MB
file_path = 'large_file.json'
target_size_mb = 10

# Generate the large JSON file
generate_large_json(file_path, target_size_mb)
