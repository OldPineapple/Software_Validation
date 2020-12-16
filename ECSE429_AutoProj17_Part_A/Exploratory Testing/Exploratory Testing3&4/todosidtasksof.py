import requests
import json

# GET todos
print("running GET...")
get_response = requests.get('http://localhost:4567/todos/1')
parsed = json.loads(get_response.text)
print("GET response:")
print(json.dumps(parsed, indent=4, sort_keys=False))

# HEAD todos
print("running HEAD...")
head_response = requests.head('http://localhost:4567/todos/1')
print("HEAD response:")
print(head_response.headers)

# POST todos
item = {
    'id': 1,
}

print("running POST...")
post_response = requests.post('http://localhost:4567/todos/2', json = item)
print("POST response:")
parsed = json.loads(post_response.text)
print(json.dumps(parsed, indent=4, sort_keys=False))

# Check new item
print("Checking new item")
print("running GET...")
get_response = requests.get('http://localhost:4567/todos')
parsed = json.loads(get_response.text)
print("GET response:")
print(json.dumps(parsed, indent=4, sort_keys=False))