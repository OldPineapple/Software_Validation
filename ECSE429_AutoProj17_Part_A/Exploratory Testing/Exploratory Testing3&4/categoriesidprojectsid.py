import requests
import json

# Post new relationship
print("Posting relationship between category 2 and project 2")
print("running POST...")
get_response = requests.post('http://localhost:4567/categories/2/projects')
parsed = json.loads(get_response.text)
print("POST response:")
print(json.dumps(parsed, indent=4, sort_keys=False))

# Check existing relationship
print("Checking existing relationship")
print("running GET...")
get_response = requests.get('http://localhost:4567/categories/2/projects')
parsed = json.loads(get_response.text)
print("GET response:")
print(json.dumps(parsed, indent=4, sort_keys=False))

# DELETE relationship
print("running DELETE...")
delete_response = requests.delete('http://localhost:4567/categories/2/projects/2')
print("DELETE response:")
print(delete_response.text)

# Check existing relationship
print("Checking existing relationship")
print("running GET...")
get_response = requests.get('http://localhost:4567/categories/2/projects')
parsed = json.loads(get_response.text)
print("GET response:")
print(json.dumps(parsed, indent=4, sort_keys=False))