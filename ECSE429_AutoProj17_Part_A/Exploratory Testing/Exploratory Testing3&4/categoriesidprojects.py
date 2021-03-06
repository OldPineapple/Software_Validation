import requests
import json

# GET todos
print("running GET...")
get_response = requests.get('http://localhost:4567/categories/1/projects')
parsed = json.loads(get_response.text)
print("GET response:")
print(json.dumps(parsed, indent=4, sort_keys=False))

# HEAD todos
print("running HEAD...")
head_response = requests.head('http://localhost:4567/categories/1/projects')
print("HEAD response:")
print(head_response.headers)

# POST todos
item = {
    'id': 1,
}

print("running POST...")
post_response = requests.post('http://localhost:4567/categories/1/projects', json = item)
print("POST response:")
parsed = json.loads(post_response.text)
print(json.dumps(parsed, indent=4, sort_keys=False))

# Check new relationship
print("Checking new relationship")
print("running GET...")
get_response = requests.get('http://localhost:4567/categories/1/projects')
parsed = json.loads(get_response.text)
print("GET response:")
print(json.dumps(parsed, indent=4, sort_keys=False))