import os
from threading import Thread 
import requests

def before_all(context):
	try:
		r = requests.get('http://127.0.0.1:4567/')
	except ConnectionError as e:
		fail("conditions not met")

def after_scenario(context, scenario):
	r = requests.get('http://127.0.0.1:4567/todos')
	r = r.json()['todos']
	for i in r:
		if not i['id'] == '1' or not i['id'] == '2':
			#print(i['id'])
			r = requests.delete('http://127.0.0.1:4567/todos/'+i['id'])
	r = requests.get('http://127.0.0.1:4567/projects')
	r = r.json()['projects']
	for i in r:
		if not i['id'] == '1':
			#print(i['id'])
			r = requests.delete('http://127.0.0.1:4567/projects/'+i['id'])
	r = requests.get('http://127.0.0.1:4567/categories')
	r = r.json()['categories']
	for i in r:
		if not i['id'] == '1' and not i['id'] == '2':
			r = requests.delete('http://127.0.0.1:4567/categories/'+i['id'])

def run_server():
	os.system("java -jar runTodoManagerRestAPI-1.5.5.jar")