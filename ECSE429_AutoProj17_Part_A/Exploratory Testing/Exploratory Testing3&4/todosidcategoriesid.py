import requests
import json

# Check existing item, should only have one
print("Checking existing item")
print("running GET...")
get_response = requests.get('http://localhost:4567/todos')
parsed = json.loads(get_response.text)
print("GET response:")
print(json.dumps(parsed, indent=4, sort_keys=False))

# DELETE relationship, existing 1:1
print("running DELETE...")
delete_response = requests.delete('http://localhost:4567/todos/1/categories/1')
print("DELETE response:")
print(delete_response.text)

# Check existing item
print("Checking existing item")
print("running GET...")
get_response = requests.get('http://localhost:4567/todos')
parsed = json.loads(get_response.text)
print("GET response:")
print(json.dumps(parsed, indent=4, sort_keys=False))