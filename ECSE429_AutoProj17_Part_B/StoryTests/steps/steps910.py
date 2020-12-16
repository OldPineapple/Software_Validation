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

def getPriority(p):
    if p == 'HIGH':
        return HIGH_id
    elif p == 'MEDIUM':
        return MEDIUM_id
    elif p == 'LOW':
        return LOW_id
    return str(-1)

@given('the server is running')
def step_impl(context):
    try:
        get_response = requests.get('http://localhost:4567/todos')
    except:
        assert False, "Server is not running."
    
@given('there is a task "{taskName}" I have known Id')
def step_impl(context, taskName):
    global task_id
    data = {
        'title': taskName
    }
    post_response = requests.post('http://localhost:4567/todos', json = data)
    parsed = json.loads(post_response.text)
    task_id = parsed['id']

@given('there are three categories HIGH, MEDIUM and LOW')
def step_impl(context):
    global HIGH_id
    global MEDIUM_id
    global LOW_id
    data1 = {
        'title': 'HIGH'
    }
    data2 = {
        'title': 'MEDIUM'
    }
    data3 = {
        'title': 'LOW'
    }
    post_response1 = requests.post('http://localhost:4567/categories', json = data1)
    parsed1 = json.loads(post_response1.text)
    HIGH_id = parsed1['id']
    context.high_id = HIGH_id
    post_response2 = requests.post('http://localhost:4567/categories', json = data2)
    parsed2 = json.loads(post_response2.text)
    MEDIUM_id = parsed2['id']
    context.medium_id = MEDIUM_id
    post_response3 = requests.post('http://localhost:4567/categories', json = data3)
    parsed3 = json.loads(post_response3.text)
    LOW_id = parsed3['id']
    context.low_id = LOW_id

@given('the task is related to the category "{oldPriority}"')
def step_impl(context, oldPriority):
    data = {
        'id': task_id
    }
    url = 'http://localhost:4567/categories/' + getPriority(oldPriority) + '/todos'
    post_response = requests.post(url, json = data)

@when('I delete the relationship between "{oldPriority}" and the task')
def step_impl(context, oldPriority):
    url = 'http://localhost:4567/categories/' + getPriority(oldPriority) + '/todos' + task_id
    delete_response = requests.delete(url)

@when('I add a new relationship between "{newPriority}" and the task')
def step_impl(context, newPriority):
    data = {
        'id': task_id
    }
    url = 'http://localhost:4567/categories/' + getPriority(newPriority) + '/todos'
    post_response = requests.post(url, json = data)
    global response
    response = post_response

@then('the priority of the task should have been changed to "{newPriority}"')
def step_impl(context, newPriority):
    url = 'http://localhost:4567/categories/' + getPriority(newPriority) + '/todos'
    get_response = requests.get(url)
    parsed = json.loads(get_response.text)
    ids = []
    for todo in parsed['todos']:
        ids.append(todo['id'])
    assert task_id in ids, get_response.text

@given('there is not a task "{taskName}" I have known Id')
def step_impl(context, taskName):
    url = 'http://localhost:4567/todos/' + task_id
    delete_response = requests.delete(url)
    url = 'http://localhost:4567/categories/' + HIGH_id + '/todos/' + task_id
    delete_response = requests.delete(url)
    url = 'http://localhost:4567/categories/' + MEDIUM_id + '/todos/' + task_id
    delete_response = requests.delete(url)
    url = 'http://localhost:4567/categories/' + LOW_id + '/todos/' + task_id
    delete_response = requests.delete(url)

@when('I add a new relationship between "{newPriority}" and the task with a wrong id "{wrongId}"')
def step_impl(context, newPriority, wrongId):
    data = {
        'id': wrongId
    }
    url = 'http://localhost:4567/categories/' + getPriority(newPriority) + '/todos'
    post_response = requests.post(url, json = data)
    global response
    response = post_response

@when('I add a new relationship between a wrong priority "{wrongP}" and the task')
def step_impl(context, wrongP):
    data = {
        'id': task_id
    }
    url = 'http://localhost:4567/categories/' + getPriority(wrongP) + '/todos'
    post_response = requests.post(url, json = data)
    global response
    response = post_response

@then('I get an error message')
def step_impl(context):
    parsed = json.loads(response.text)
    assert parsed['errorMessages'] is not None

@when('I modify the description of the task to "{newD}"')
def step_impl(context, newD):
    global response
    data = {
        'description': newD
    }
    url = 'http://localhost:4567/todos/' + task_id
    post_reponse = requests.post(url, json = data)
    response = post_reponse

@then('the description of the task "{taskName}" should have been changed to "{newD}"')
def step_impl(context, taskName, newD):
    url = 'http://localhost:4567/todos/' + task_id
    get_reponse = requests.get(url)
    parsed = json.loads(get_reponse.text)
    des = parsed['todos'][0]['description']
    assert des == newD

@when('I delete the task')
def step_impl(context):
    url = 'http://localhost:4567/todos/' + task_id
    delete_response = requests.delete(url)

@when('create a new task of "{taskName}" with the new description "{newD}"')
def step_impl(context, taskName, newD):
    global task_id
    data = {
        'title': taskName,
        'description': newD
    }
    post_response = requests.post('http://localhost:4567/todos', json = data)
    parsed = json.loads(post_response.text)
    task_id = parsed['id']

@when('I modify the description of the task using a wrong id "{wrongId}" to "{newD}"')
def step_impl(context, newD, wrongId):
    global response
    data = {
        'description': newD
    }
    url = 'http://localhost:4567/todos/' + wrongId
    post_reponse = requests.post(url, json = data)
    response = post_reponse