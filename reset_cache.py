import json
import sys

filename = sys.argv[1]

with open(filename, 'w') as f:
    json.dump([], f)
