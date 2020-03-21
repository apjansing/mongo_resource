#!/usr/local/bin/python
import json
import sys
import os
from os.path import join
from functools import reduce 

if __name__ == "__main__":
  operations = {
    'multiply': lambda a, b : a * b,
    'divide': lambda a, b : a / b,
    'add': lambda a, b : a + b,
    'subtract': lambda a, b : a - b
  }

  updated_keys = {
    'multiply': 'multiplied',
    'divide': 'divided',
    'add': 'added',
    'subtract': 'subtracted'
  }

  filenames = os.listdir(sys.argv[1])
  for filename in filenames:
    print(filename)
    with open(filename, 'r') as f:
      json = json.load(f)
      new_json = json.copy()
      for item in json.items():
        key = item[0]
        if key in operations.keys():
          op = operations[key]
          new_json[updated_keys[key]] = reduce(op, json[key])
          print(new_json)
    with open(filename, 'w') as f:
      json.dump(new_json, f)