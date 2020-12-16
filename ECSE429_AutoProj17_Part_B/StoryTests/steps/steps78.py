from behave import *
import requests
import json
from behave.log_capture import capture
from behave import fixture, use_fixture

task_id = ''    # global task id that can be used within each scenario
HIGH_id = ''    # global category id that can be used within each scenario
MEDIUM_id = ''  # global category id that can be used within each scenario
LOW_id = ''     # global category id that can be used within each scenario
response = ''   # global response that can be used within each scenario

@given('there is an incomplete task "{taskName}"')
def step_impl(context,taskName):
	data = {"title":taskName,"doneStatus":False}
	r = requests.post('http://127.0.0.1:4567/todos',json=data)
	projectsID = context.id[0]
	data = {'id':r.json()['id']}
	r = requests.post('http://127.0.0.1:4567/projects/'+projectsID+'/tasks',json=data)

@given('there is a completed task')
def step_impl(context):
	data = {"title":"Reading","doneStatus":True}
	r = requests.post('http://127.0.0.1:4567/todos',json=data)
	projectsID = context.id[0]
	data = {'id':r.json()['id']}
	r = requests.post('http://127.0.0.1:4567/projects/'+projectsID+'/tasks',json=data)

@given('I forgot the class id')
def step_impl(context):
	context.id = []

@given('there is an incomplete task "{taskName}" with unknown task id')
def step_impl(context,taskName):
	context.id = []
	data = {"title":taskName,"doneStatus":False}
	r = requests.post('http://127.0.0.1:4567/todos',json=data)
	priorityID = context.high_id
	context.id.append(priorityID)
	data = {'id':r.json()['id']}
	r = requests.post('http://127.0.0.1:4567/categories/'+priorityID+'/todos',json=data)

@given('there is a completed task with HIGH priority')
def step_impl(context):
	context.id = []
	data = {"title":'Reading',"doneStatus":True}
	r = requests.post('http://127.0.0.1:4567/todos',json=data)
	priorityID = context.high_id
	context.id.append(priorityID)
	data = {'id':r.json()['id']}
	r = requests.post('http://127.0.0.1:4567/categories/'+priorityID+'/todos',json=data)

@given('I forgot the category id')
def step_impl(context):
	context.id = []

@when('I send a get API with class id')
def step_impl(context):
    url = 'http://127.0.0.1:4567/projects/' + context.id[0] + '/tasks'
    context.response = requests.get(url,params = {'doneStatus':'false'})
    context.result = context.response.json()

@when('I send a get API with invalid category id')
def step_impl(context):
    url = 'http://127.0.0.1:4567/categories/' + '100' + '/todos'
    context.response = requests.get(url)
    context.result = context.response.json()

@when('I query class id using valid class name "{className}"')
def step_impl(context, className):
	url = 'http://127.0.0.1:4567/projects'
	params = {'title':className}
	get_response = requests.get(url,params=params)
	context.result = get_response.json()
	if context.result['projects'][0]['title'] == className:
		context.id.append(context.result['projects'][0]['id'])

@when ('I send a get API with high priority category id todos')
def step_impl(context):
	url = 'http://127.0.0.1:4567/categories/' + HIGH_id + '/todos'
	get_response = requests.get(url,params={'doneStatus':'false'})
	print(get_response.json())
	context.result = get_response.json()

@when ('I query category id using valid category name "{priority}"')
def step_impl(context, priority):
	url = 'http://127.0.0.1:4567/categories'
	params = {'title':priority}
	get_response = requests.get(url,params=params)
	context.result = get_response.json()
	if context.result['categories'][0]['title'] == priority:
		context.id.append(context.result['categories'][0]['id'])

@then('I should receive all incomplete tasks "{taskName}" of that class')
def step_impl(context,taskName):
    assert context.result['todos'][0]['title'] == taskName and context.result['todos'][0]['doneStatus'] == 'false'

@then('I should get an error message')
def step_impl(context):
	if context.response.status_code == 200:
		print('It should return an error message')

@then('I should receive all incomplete HIGH priority tasks "{taskName}"')
def step_impl(context,taskName):
	assert context.result['todos'][0]['title'] == taskName and context.result['todos'][0]['doneStatus'] == 'false'