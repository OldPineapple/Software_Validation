import requests
import json

print("running GET...")
get_response = requests.get('http://localhost:4567/docs')
print(get_response.text)