from behave import *
import requests
import json
from behave.log_capture import capture
from behave import fixture, use_fixture

'''
fixture_registry1 = {
    "fixture.clean": clean,
}
fixture_registry2 = {
    "fixture.clean": fixture_call_params(clean),
}
'''

@given('there is a class "{className}" projects I have known Id')
def step_impl(context,className):
	context.id = []
	context.classData = {'title':className}
	data = {'title':className}
	r = requests.post('http://127.0.0.1:4567/projects',json=data)
	res = r.json()
	context.id.append(res['id'])

@given('I have a unnecessary task "{taskName}" in it')
def step_impl(context,taskName):
	data = {'title':taskName}
	r = requests.post('http://127.0.0.1:4567/todos',json=data)
	res = r.json()
	context.id.append(res['id'])
	data = {'id':res['id']}
	r = requests.post('http://127.0.0.1:4567/todos/'+context.id[0],json=data)

	
@given('there is a class "{className}" projects I have not known Id')	
def step_impl(context,className):
	data = {'title':className}
	r = requests.post('http://127.0.0.1:4567/projects',json=data)
@given('there is a class "{className}" projects I have known a wrong Id')
def step_impl(context,className):
	context.id = []
	context.classData = {'title':className}
	data = {'title':className}
	r = requests.post('http://127.0.0.1:4567/projects',json=data)
	res = r.json()
	context.id.append("100")

@when('I send a delete API "{APIdelete}"')
def step_impl(context,APIdelete):
	idCounts = APIdelete.count(":id")
	for i in range(idCounts):
		APIdelete = APIdelete.replace(":id",context.id[i],1)
	r = requests.delete('http://127.0.0.1:4567'+APIdelete)
	context.response = r
	
@when('I send a get Request "{APIget}" about projects Course')
def step_impl(context,APIget):
	idCounts = APIget.count(":id")
	for i in range(idCounts):
		APIget = APIget.replace(":id",context.id[i],1)
	r = requests.get('http://127.0.0.1:4567'+APIget)
	context.result = r.json()
@when('I use a get api "{APIget}" with parameter "{className}" string as a filter to get id')
def step_impl(context,APIget,className):
	idCounts = APIget.count(":id")
	for i in range(idCounts):
		APIget = APIget.replace(":id",context.id[i],1)
	r = requests.get('http://127.0.0.1:4567'+APIget,params = {'title':className})
	context.id = []
	context.id.append(r.json()['projects'][0]['id'])

@when('I send a put API "{APIpost}" with "{data}"')
def step_impl(context,APIpost,data):
	idCounts = APIpost.count(":id")
	for i in range(idCounts):
		APIpost = APIpost.replace(":id",context.id[i],1)
	data = json.loads(data)
	for i in data.keys():
		context.classData[i] = data[i]
	r = requests.put('http://127.0.0.1:4567'+APIpost,json = context.classData)
	context.response = r

@when('I send a post api "{APIpost}" with "{className}"')
def step_impl(context,APIpost,className):
	data = {'title':className}
	idCounts = APIpost.count(":id")
	for i in range(idCounts):
		APIpost = APIpost.replace(":id",context.id[i],1)
	r = requests.post('http://127.0.0.1:4567'+APIpost,json = data)
	context.response = r
	context.id = []
	context.id.append(r.json()['id'])
	print(len(context.id))
	
@when('I send a post api "{APIpost}" with both "{className}" and "{description}"')
def step_impl(context,APIpost,className,description):
	data = {'title':className,'description':description}
	idCounts = APIpost.count(":id")
	for i in range(idCounts):
		APIget = APIpost.replace(":id",context.id[i],1)
	r = requests.post('http://127.0.0.1:4567'+APIpost,json = data)
	context.response = r
	context.id = []
	context.id.append(r.json()['id'])
	
@when('I send a post api "{APIpost}" with "{className}" with id')
def step_impl(context,APIpost,className):
	data = {'title':className,'id':'9'}
	idCounts = APIpost.count(":id")
	for i in range(idCounts):
		APIget = APIpost.replace(":id",context.id[i],1)
	r = requests.post('http://127.0.0.1:4567'+APIpost,json = data)
	context.response = r
@when('I send a delete API "{APIdelete}" with wrong id')
def step_impl(context,APIdelete):
	idCounts = APIdelete.count(":id")
	for i in range(idCounts):
		APIdelete = APIdelete.replace(":id",str(int(context.id[i])+1),1)
	r = requests.delete('http://127.0.0.1:4567'+APIdelete)
	context.response = r
	
@then('I will get a projects with right "{className}"')
def step_impl(context,className):
	assert context.result['projects'][0]['title'] == className
@then('I will get a project with right "{className}" and "{description}"')
def step_impl(context,className,description):
	assert context.result['projects'][0]['title'] == className and context.result['projects'][0]['description'] == description

@then('check all the projects. there is no projects with this "{className}"')
def step_impl(context,className):
	for i in context.result['projects']:
		assert not i['title'] == className
@then('the task should be not in the project Course')
def step_impl(context):
	assert not 'tasks' in context.result['projects'][0] or not {'id':context.id[1]} in context.result['projects'][0]['tasks'] 
@then('I should get a error message "{error}"')
def step_impl(context,error):
	assert error in context.response.json()["errorMessages"][0]
	
	
