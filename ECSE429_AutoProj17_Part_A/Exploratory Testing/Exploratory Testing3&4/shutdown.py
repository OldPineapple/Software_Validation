import requests
import json

print("running GET...")
get_response = requests.get('http://localhost:4567/shutdown')
print(get_response.text)