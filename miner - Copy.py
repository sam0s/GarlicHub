import subprocess
import json
from os import path

with open('currentStats.json') as json_data:
    d = json.load(json_data)
    print d['stats'][2]['hash']
