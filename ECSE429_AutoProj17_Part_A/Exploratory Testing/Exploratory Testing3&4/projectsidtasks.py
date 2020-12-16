import requests
import json

# GET todos
print("running GET...")
get_response = requests.get('http://localhost:4567/projects/1/tasks')
parsed = json.loads(get_response.text)
print("GET response:")
print(json.dumps(parsed, indent=4, sort_keys=False))

# HEAD todos
print("running HEAD...")
head_response = requests.head('http://localhost:4567/projects/1/tasks')
print("HEAD response:")
print(head_response.headers)

# POST todos
todo = {
    'title': 'ui officia deserunta',
    'doneStatus': True,
    'description': 'ex ea commodo consea',
}

print("running POST...")
post_response_1 = requests.post('http://localhost:4567/todos', json = todo)
print("POST response:")
parsed = json.loads(post_response_1.text)
print(json.dumps(parsed, indent=4, sort_keys=False))

item = {
    'id': 3,
}

print("running POST...")
post_response_2 = requests.post('http://localhost:4567/projects/1/tasks', json = item)
print("POST response:")
parsed = json.loads(post_response_2.text)
print(json.dumps(parsed, indent=4, sort_keys=False))

# Check new item
print("Checking new item")
print("running GET...")
get_response = requests.get('http://localhost:4567/todos')
parsed = json.loads(get_response.text)
print("GET response:")
print(json.dumps(parsed, indent=4, sort_keys=False))