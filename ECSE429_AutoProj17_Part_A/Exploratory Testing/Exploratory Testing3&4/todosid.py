import requests
import json

# GET todos, existing items with id 1 and 2
print("running GET...")
get_response = requests.get('http://localhost:4567/todos/2')
parsed = json.loads(get_response.text)
print("GET response:")
print(json.dumps(parsed, indent=4, sort_keys=False))

# HEAD todos
print("running HEAD...")
head_response = requests.head('http://localhost:4567/todos/2')
print("HEAD response:")
print(head_response.headers)

# POST todos, existing items with id 1 and 2
item = {
    'title': 'ui officia deserunta',
    'doneStatus': True,
    'description': 'ex ea commodo consea',
}

print("running POST...")
post_response = requests.post('http://localhost:4567/todos/1', json = item)
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

# PUT todos, existing items with id 1 and 2
item = {
    'title': 'ui officia deserunta',
    'doneStatus': True,
    'description': 'ex ea commodo consea',
}

print("running PUT...")
put_response = requests.put('http://localhost:4567/todos/2', json = item)
print("PUT response:")
parsed = json.loads(put_response.text)
print(json.dumps(parsed, indent=4, sort_keys=False))

# Check new item
print("Checking new item")
print("running GET...")
get_response = requests.get('http://localhost:4567/todos')
parsed = json.loads(get_response.text)
print("GET response:")
print(json.dumps(parsed, indent=4, sort_keys=False))

# DELETE todos, existing items with id 1 and 2

print("running DELETE...")
delete_response = requests.delete('http://localhost:4567/todos/2')
print("DELETE response:")
print(delete_response.text)

# Check existing item, should only have one
print("Checking existing item")
print("running GET...")
get_response = requests.get('http://localhost:4567/todos')
parsed = json.loads(get_response.text)
print("GET response:")
print(json.dumps(parsed, indent=4, sort_keys=False))