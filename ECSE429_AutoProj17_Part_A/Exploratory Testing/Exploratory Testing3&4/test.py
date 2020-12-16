import requests
import json

item = {
    'title': 'ui officia deserunta',
    'doneStatus': True,
    'description': 'ex ea commodo consea',
}
#post_response = requests.post('http://localhost:4567/todos', json = item)
get_response = requests.get('http://localhost:4567/todos')

parsed = json.loads(get_response.text)
print(json.dumps(parsed, indent=4, sort_keys=False))