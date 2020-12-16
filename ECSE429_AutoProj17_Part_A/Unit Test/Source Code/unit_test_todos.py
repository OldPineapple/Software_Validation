import json
import os
import unittest
import subprocess
import sys
from threading import Thread
import time
from multiprocessing import Process
import socket
try:
	import requests
	from requests.exceptions import ConnectionError
except Exception as e:
	subprocess.check_call([sys.executable,"-m","pip","install","requests"])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
URL = "http://localhost:4567/"
class CorruptDataFormat(unittest.TestCase):
	URL = "http://localhost:4567/"
	
	def setUp(self):
		try:
			r = requests.get(URL)
		except ConnectionError as e:
			self.fail("conditions not met")
	
	def test_corrupt_json(self):
		data = {"title":'test_post',"doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos",data = json.dumps(data)[0:-1])
		self.assertEqual(r.status_code,400)
		self.assertTrue("java.io.EOFException" in r.json()['errorMessages'][0])
	
	def test_corrupt_XML(self):
		data_XML = "<todo><doneStatus>false</doneStatus><description>lamco laboris nisi u</description><title>e irure dolor in rep</title></todo>"
		headers = {'Content-Type': 'application/xml'}
		r = requests.post(URL+"todos",data = data_XML[0:-1],headers = headers)
		self.assertEqual(r.status_code,400)
		self.assertTrue("Misshaped element" in r.json()['errorMessages'][0])
class TodosTest(unittest.TestCase):
	URL = "http://localhost:4567/"
	
	def setUp(self):
		try:
			r = requests.get(URL)
		except ConnectionError as e:
			self.fail("conditions not met")
	
	def test_curlCommand(self):
		def order(x):
			return x['id']
		answer = b'{"todos":[{"id":"1","title":"scan paperwork","doneStatus":"false","description":"","categories":[{"id":"1"}],"tasksof":[{"id":"1"}]},{"id":"2","title":"file paperwork","doneStatus":"false","description":"","tasksof":[{"id":"1"}]}]}'
		result = subprocess.check_output(["curl",URL+"todos"])
		result = json.loads(result)
		result['todos'].sort(key = order)
		answer = json.loads(answer)
		answer['todos'].sort(key = order)
		self.assertEqual(result,answer)
	def test_curlCommand(self):
		result = subprocess.check_call(["curl",URL+"todos"])
		self.assertEqual(result,0)
	def test_get(self):
		def order(x):
			return x['id']
		answer = '{"todos":[{"id":"1","title":"scan paperwork","doneStatus":"false","description":"","categories":[{"id":"1"}],"tasksof":[{"id":"1"}]},{"id":"2","title":"file paperwork","doneStatus":"false","description":"","tasksof":[{"id":"1"}]}]}'
		r = requests.get(URL+"todos")
		r = r.json()
		r['todos'].sort(key = order)
		answer = json.loads(answer)
		answer['todos'].sort(key = order)
		self.assertEqual(r,answer)
	
	def test_wrongURL(self):
		r = requests.get(URL+"todo")
		self.assertEqual(r.status_code,404)
	def test_get_with_urlParameter(self):
		d = {"title":"scan paperwork"}
		r = requests.get(URL+"todos",params = d)
		data = r.json()
		answer = json.loads('{"id":"1","title":"scan paperwork","doneStatus":"false","description":"","categories":[{"id":"1"}],"tasksof":[{"id":"1"}]}')
		self.assertEqual(len(data["todos"]),1)
		self.assertEqual(data["todos"][0],answer)
	def test_get_with_wrong_urlParameter_value(self):
		d = {"title":"scan paperworks"}
		r = requests.get(URL+"todos",params = d)
		data = r.json()
		self.assertEqual(len(data["todos"]),0)
	def test_get_with_non_existing_urlParameter(self):
		print('test_get_with_non_existing_urlParameter\n')
		d = {"titles":"scan paperwork"}
		r = requests.get(URL+"todos",params = d)
		data = r.json()
		print(len(data["todos"]),"length is not right, I think this is a bug\n")
		self.assertEqual(len(data["todos"]),2)
	def test_head(self):
		r = requests.head(URL+"todos")
		self.assertEqual(r.status_code,200)
		self.assertEqual(len(r.content),0)
	def test_post(self):
		data = {"title":"test_post","doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_id(self):
		data = {"id":"1","title":"test_post","doneStatus":False,"description":"test_post"}
		r = requests.post("http://localhost:4567/todos",json = data)
		self.assertEqual(r.json()['errorMessages'][0],'Invalid Creation: Failed Validation: Not allowed to create with id')
	def test_post_with_no_data(self):
		r = requests.post(URL+"todos")
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'title : field is mandatory')
	def test_post_with_empty_data(self):
		r = requests.post(URL+"todos",json = {})
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'title : field is mandatory')
	def test_post_with_space_title(self):
		data = {"title":" ","doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Failed Validation: title : can not be empty')
	def test_post_with_no_doneStatus(self):
		data = {"title":"test_post","description":"test_post"}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		self.assertEqual(response['doneStatus'],'false')
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_no_description(self):
		data = {"title":"test_post","doneStatus":True,}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["doneStatus"] = "true"
		data["description"] = ""
		self.assertEqual(response,data)
		self.assertEqual(response['description'],'')
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_empty_description(self):
		data = {"title":"test_post","doneStatus":False,"description":""}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_space_description(self):
		data = {"title":"test_post","doneStatus":False,"description":" "}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_empty_title(self):
		data = {"title":"","doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Failed Validation: title : can not be empty')
	def test_post_with_str_doneStatus(self):
		data = {"title":"test_post","doneStatus":"False","description":"test_post"}
		r = requests.post(URL+"todos",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Failed Validation: doneStatus should be BOOLEAN')
	def test_post_with_wrong_title_type_float(self):
		data = {"title":1.0,"doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["title"] = "1.0"
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		self.assertEqual(response['title'],'1.0')
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_wrong_title_type_boolean(self):
		data = {"title":False,"doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["title"] = "false"
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		self.assertEqual(response['title'],'false')
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_wrong_title_type_empty_list(self):
		data = {"title":[],"doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'title : field is mandatory')
	def test_post_with_wrong_title_type_list(self):
		data = {"title":['aa','sss'],"doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["title"] = "sss"
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		self.assertEqual(response['title'],'sss')
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_wrong_title_type_empty_dict(self):
		data = {"title":{},"doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'title : field is mandatory')
	def test_post_with_wrong_title_type_dict(self):
		data = {"title":{'aaa':'1'},"doneStatus":False,"description":'test_post'}
		r = requests.post(URL+"todos",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Cannot reference fields on non object fields: title')
	def test_post_with_wrong_description_type_int(self):
		data = {"title":'test_post',"doneStatus":False,"description":1}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["description"] = "1.0"
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		self.assertEqual(response['description'],'1.0')
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_wrong_description_type_float(self):
		data = {"title":'test_post',"doneStatus":False,"description":1.0}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["description"] = "1.0"
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		self.assertEqual(response['description'],'1.0')
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_wrong_description_type_boolean(self):
		data = {"title":'test_post',"doneStatus":False,"description":True}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["description"] = "true"
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		self.assertEqual(response['description'],'true')
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_wrong_description_type_empty_list(self):
		data = {"title":'test_post',"doneStatus":False,"description":[]}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["description"] = ""
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		self.assertEqual(response['description'],'')
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_wrong_description_type_list(self):
		data = {"title":'test_post',"doneStatus":False,"description":['sss','aa']}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["description"] = "aa"
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		self.assertEqual(response['description'],'aa')
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_wrong_title_type_int(self):
		data = {"title":1,"doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["title"] = "1.0"
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		self.assertEqual(response['title'],'1.0')
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_wrong_description_type_empty_dict(self):
		data = {"title":'test_post',"doneStatus":False,"description":{}}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		id = response["id"]
		data["id"] = id
		data["description"] = ""
		data["doneStatus"] = "false"
		self.assertEqual(response,data)
		self.assertEqual(response['description'],'')
		r = requests.get(URL+"todos")
		result = r.json()
		self.assertTrue(response in result["todos"])
		self.recover(id)
	def test_post_with_wrong_description_type_dict(self):
		data = {"title":'test_post',"doneStatus":False,"description":{"sss":"1"}}
		r = requests.post(URL+"todos",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Cannot reference fields on non object fields: description')
	def test_post_with_extra_parameter(self):
		data = {"title":'test_post',"doneStatus":False,"description":"test_post","titles":"test_post"}
		r = requests.post(URL+"todos",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find field: titles')
	def test_method_non_exist(self):
		r = requests.delete(URL+'todos')
		self.assertEqual(r.status_code,405)
		self.assertEqual(len(r.content),0)
	def recover(self,id):
		r = requests.delete(URL+"todos/"+id)
		
class TodosIdTest(unittest.TestCase):
	
	def setUp(self):
		try:
			r = requests.get(URL)
		except ConnectionError as e:
			self.fail("conditions not met")
	def test_get(self):
		id = 1
		answer = '{"todos": [{"id": "1", "title": "scan paperwork", "doneStatus": "false", "description": "", "tasksof": [{"id": "1"}], "categories": [{"id": "1"}]}]}'
		r = requests.get(URL+"todos/"+str(id))
		self.assertEqual(r.json(),json.loads(answer))
	def test_get_xml(self):
		id = 1
		answer = b'<todos><todo><doneStatus>false</doneStatus><description/><tasksof><id>1</id></tasksof><id>1</id><categories><id>1</id></categories><title>scan paperwork</title></todo></todos>'
		headers = {'Accept': 'application/xml'}
		r = requests.get(URL+"todos/"+str(id),headers = headers)
		self.assertEqual(r.content,answer)
	def test_get_wrong_id(self):
		id = 3
		r = requests.get(URL+"todos/"+str(id))
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find an instance with todos/3')
	def test_post(self):
		id = 1
		answer = requests.get(URL+"todos/"+str(id)).json()
		
		data = {"title":'test_post',"doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		data['id'] = str(id)
		data['doneStatus'] = 'false'
		self.assertTrue(response['id']==data['id'] and response['doneStatus']==data['doneStatus'] and response['title']==data['title'] and response['description']==data['description'])
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertTrue(response in result['todos'])
		self.recover(answer)
	def test_post_no_data(self):
		id = 1
		answer = requests.get(URL+"todos/"+str(id)).json()
		r = requests.post(URL+"todos/"+str(id))
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertTrue(result,answer)
	def test_post_with_empty_data(self):
		id = 1
		answer = requests.get(URL+"todos/"+str(id)).json()
		r = requests.post(URL+"todos/"+str(id),json={})
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertTrue(result,answer)
	def test_post_with_no_title(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'test_post'
		data = {"doneStatus":True,"description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_empty_title(self):
		id = 1
		data = {"title":"","doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Failed Validation: title : can not be empty')
	def test_post_with_space_title(self):
		id = 1
		data = {"title":" ","doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Failed Validation: title : can not be empty')
	def test_post_with_no_doneStatus(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['description'] = 'test_post'
		data = {"title":"test_post","description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_wrong_id(self):
		id = 3
		data = {"title":'test_post',"doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'No such todo entity instance with GUID or ID 3 found')
	def test_post_with_no_description(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		data = {"title":"test_post","doneStatus":True}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_empty_description(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = ''
		data = {"title":"test_post","doneStatus":True,"description":""}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def recover(self,recoverData):
		recoverData = recoverData['todos'][0]
		id = recoverData.pop('id',None)
		if recoverData['doneStatus'] == 'true':
			recoverData['doneStatus'] = True
		else: 
			recoverData['doneStatus'] = False
		r = requests.post(URL+"todos/"+str(id),json = recoverData)
	def test_post_with_str_doneStatus(self):
		id = 1
		data = {"title":"test_post","doneStatus":"False","description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Failed Validation: doneStatus should be BOOLEAN')
	def test_post_with_wrong_description_type_boolean(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'true'
		data = {"title":"test_post","doneStatus":True,"description":True}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_space_description(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = ' '
		data = {"title":"test_post","doneStatus":True,"description":" "}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_wrong_title_type_boolean(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'true'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'test_post'
		data = {"title":True,"doneStatus":True,"description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_wrong_description_type_dict(self):
		id = 1
		data = {"title":'test_post',"doneStatus":False,"description":{"sss":"1"}}
		r = requests.post(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Cannot reference fields on non object fields: description')
	def test_post_with_wrong_title_type_dict(self):
		id = 1
		data = {"title":{"sss":"1"},"doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Cannot reference fields on non object fields: title')
	def test_post_with_wrong_description_type_empty_dict(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = ''
		data = {"title":"test_post","doneStatus":True,"description":{}}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_wrong_title_type_empty_dict(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'test_post'
		data = {"title":{},"doneStatus":True,"description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_wrong_description_type_empty_list(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = ''
		data = {"title":"test_post","doneStatus":True,"description":[]}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_wrong_title_type_empty_list(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'test_post'
		data = {"title":[],"doneStatus":True,"description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_wrong_description_type_float(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = '1.0'
		data = {"title":"test_post","doneStatus":True,"description":1.0}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_wrong_title_type_float(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = '1.0'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'test_post'
		data = {"title":1.0,"doneStatus":True,"description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_wrong_description_type_int(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = '1.0'
		data = {"title":"test_post","doneStatus":True,"description":1}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_wrong_title_type_int(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = '1.0'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'test_post'
		data = {"title":1,"doneStatus":True,"description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_wrong_description_type_list(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'aa'
		data = {"title":"test_post","doneStatus":True,"description":["sss","aa"]}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_wrong_title_type_list(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'aa'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'test_post'
		data = {"title":["sss","aa"],"doneStatus":True,"description":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_post_with_extra_parameter(self):
		id = 1
		data = {"title":'test_post',"doneStatus":False,"description":"test_post","titles":"test_post"}
		r = requests.post(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find field: titles')	
	def test_put(self):
		id = 1
		answer = requests.get(URL+"todos/"+str(id)).json()
		
		data = {"title":'test_post',"doneStatus":False,"description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		data['id'] = str(id)
		data['doneStatus'] = 'false'
		self.assertTrue(response['id']==data['id'] and response['doneStatus']==data['doneStatus'] and response['title']==data['title'] and response['description']==data['description'])
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertTrue(response in result['todos'])
		self.recover(answer)
	def test_put_wrong_id(self):
		id = 3
		data = {"title":'test_post',"doneStatus":False,"description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Invalid GUID for 3 entity todo')
	def test_put_no_data(self):
		id = 1
		answer = requests.get(URL+"todos/"+str(id)).json()
		r = requests.put(URL+"todos/"+str(id))
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertTrue(result,answer)
	def test_put_with_empty_data(self):
		id = 1
		answer = requests.get(URL+"todos/"+str(id)).json()
		r = requests.put(URL+"todos/"+str(id),json={})
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertTrue(result,answer)
	def test_put_with_no_title(self):
		id = 1
		data = {"doneStatus":True,"description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'title : field is mandatory')
	def test_put_with_empty_title(self):
		id = 1
		data = {"title":"","doneStatus":False,"description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Failed Validation: title : can not be empty')
	def test_put_with_space_title(self):
		id = 1
		data = {"title":" ","doneStatus":False,"description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Failed Validation: title : can not be empty')
	def test_put_with_no_doneStatus(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['description'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'false'
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":"test_post","description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_no_description(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":"test_post","doneStatus":True}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_empty_description(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = ''
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":"test_post","doneStatus":True,"description":""}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_space_description(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = ' '
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":"test_post","doneStatus":True,"description":" "}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_str_doneStatus(self):
		id = 1
		data = {"title":"test_post","doneStatus":"False","description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Failed Validation: doneStatus should be BOOLEAN')
	def test_put_with_wrong_description_type_boolean(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'true'
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":"test_post","doneStatus":True,"description":True}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_wrong_title_type_boolean(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'true'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'test_post'
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":True,"doneStatus":True,"description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_wrong_description_type_dict(self):
		id = 1
		data = {"title":'test_post',"doneStatus":False,"description":{"sss":"1"}}
		r = requests.put(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Cannot reference fields on non object fields: description')
	def test_put_with_wrong_title_type_dict(self):
		id = 1
		data = {"title":{"sss":"1"},"doneStatus":False,"description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Cannot reference fields on non object fields: title')
	def test_put_with_wrong_description_type_empty_dict(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = ''
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":"test_post","doneStatus":True,"description":{}}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_wrong_title_type_empty_dict(self):
		id = 1
		data = {"title":{},"doneStatus":True,"description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'title : field is mandatory')
	def test_put_with_wrong_description_type_empty_list(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = ''
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":"test_post","doneStatus":True,"description":[]}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_wrong_title_type_empty_list(self):
		id = 1
		data = {"title":[],"doneStatus":True,"description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'title : field is mandatory')
	def test_put_with_wrong_description_type_float(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = '1.0'
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":"test_post","doneStatus":True,"description":1.0}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_wrong_title_type_float(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = '1.0'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'test_post'
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":1.0,"doneStatus":True,"description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_wrong_description_type_int(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = '1.0'
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":"test_post","doneStatus":True,"description":1}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_wrong_title_type_int(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = '1.0'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'test_post'
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":1,"doneStatus":True,"description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_wrong_description_type_list(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'test_post'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'aa'
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":"test_post","doneStatus":True,"description":["sss","aa"]}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_wrong_title_type_list(self):
		id = 1
		recoverData = requests.get(URL+"todos/"+str(id)).json()
		answer = requests.get(URL+"todos/"+str(id)).json()
		answer['todos'][0]['title'] = 'aa'
		answer['todos'][0]['doneStatus'] = 'true'
		answer['todos'][0]['description'] = 'test_post'
		answer['todos'][0].pop('categories',None)
		answer['todos'][0].pop('tasksof',None)
		data = {"title":["sss","aa"],"doneStatus":True,"description":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		response = r.json()
		r = requests.get(URL+"todos/"+str(id))
		result = r.json()
		self.assertEqual(result,answer)
		self.recover(recoverData)
	def test_put_with_extra_parameter(self):
		id = 1
		data = {"title":'test_post',"doneStatus":False,"description":"test_post","titles":"test_post"}
		r = requests.put(URL+"todos/"+str(id),json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find field: titles')
	def test_delete(self):
		answer = requests.get(URL+"todos").json()
		data = {"title":"test_post","doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		r = requests.get(URL+"todos").json()
		self.assertEqual(len(r['todos']),3)
		id = response['id']
		r = requests.delete(URL+"todos/"+id)
		result = requests.get(URL+"todos").json()
		self.assertEqual(result,answer)
	def test_double_delete(self):
		answer = requests.get(URL+"todos").json()
		data = {"title":"test_post","doneStatus":False,"description":"test_post"}
		r = requests.post(URL+"todos",json = data)
		response = r.json()
		r = requests.get(URL+"todos").json()
		self.assertEqual(len(r['todos']),3)
		id = response['id']
		r = requests.delete(URL+"todos/"+id)
		result = requests.get(URL+"todos").json()
		self.assertEqual(result,answer)
		r = requests.delete(URL+"todos/"+id)
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find any instances with todos/'+id)
	def test_delete_non_exist(self):
		r = requests.delete(URL+"todos/"+'3')
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find any instances with todos/3')

class TodosIdTaskofTester(unittest.TestCase):
	def setUp(self):
		try:
			r = requests.get(URL)
		except ConnectionError as e:
			self.fail("conditions not met")
	def test_get(self):
		answer = requests.get(URL+"projects/1").json()
		result = requests.get(URL+"todos/1/tasksof").json()
		self.assertEqual(result,answer)
	def test_get_with_wrong_id(self):
		print('test_get_with_wrong_id\n')
		id = 3
		result = requests.get(URL+"todos/"+str(id)+"/tasksof")
		print('this is strange, it should be a error code instead of 2 copy of project information\n')
		self.assertEqual(result.status_code,200)
	def test_post(self):
		id = 1
		projectData = {'title':'test_post','completed':False,'active':False,'description':'test_post'}
		addResponse = requests.post(URL+"projects",json = projectData)
		pid = addResponse.json()['id']
		data = {'id':pid}
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = data)
		projectData['id'] = pid
		projectData['tasks'] = [{'id':'1'}]
		projectData['completed'] = 'false'
		projectData['active'] = 'false'
		r = requests.get(URL+"todos/1/tasksof").json()['projects']
		self.assertTrue(projectData in r)
		r = requests.delete(URL+"todos/"+str(id)+"/tasksof/"+pid)
		r = requests.delete(URL+"projects/"+pid)
	def test_post_repeat(self):
		answer = requests.get(URL+"todos/1/tasksof").json()
		data = {'id':'1'}
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = data)
		result = requests.get(URL+"todos/1/tasksof").json()
		self.assertEqual(result,answer)
	def test_post_no_data(self):
		print('test_post_no_data\n')
		print('the system should do nothing,but it create a new project and add a relation\n')
		answer = requests.get(URL+"todos/1/tasksof").json()
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/tasksof")
		pid = r.json()['id']
		result = requests.get(URL+"todos/1/tasksof").json()
		self.assertTrue(result != answer)
		r = requests.delete(URL+"todos/"+str(id)+"/tasksof/"+pid)
		r = requests.delete(URL+"projects/"+pid)
	def test_post_empty_data(self):
		print('test_post_empty_data\n')
		print('the system should do nothing,but it create a new project and add a relation\n')
		answer = requests.get(URL+"todos/1/tasksof").json()
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = {})
		pid = r.json()['id']
		result = requests.get(URL+"todos/1/tasksof").json()
		self.assertTrue(result!=answer)
		r = requests.delete(URL+"todos/"+str(id)+"/tasksof/"+pid)
		r = requests.delete(URL+"projects/"+pid)
	def test_post_non_existing_id(self):
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = {'id':'2'})
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find thing matching value for id')
	def test_post_empty_id(self):
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = {'id':''})
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find thing matching value for id')
	def test_post_space_id(self):
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = {'id':' '})
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find thing matching value for id')
	def test_post_int_id(self):
		projectData1 = {'title':'test_post','completed':False,'active':False,'description':'test_post'}
		addResponse = requests.post(URL+"projects",json = projectData1)
		pid = addResponse.json()['id']
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = {'id':int(pid)})
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find thing matching value for id')
		r = requests.delete(URL+"projects/"+pid)
	def test_post_id_list(self):
		projectData1 = {'title':'test_post','completed':False,'active':False,'description':'test_post'}
		projectData2 = {'title':'test_post','completed':False,'active':False,'description':'test_post'}
		addResponse = requests.post(URL+"projects",json = projectData1)
		pid1 = addResponse.json()['id']
		addResponse = requests.post(URL+"projects",json = projectData2)
		pid2 = addResponse.json()['id']
		data = {'id':[pid1,pid2]}
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Invalid Creation: Failed Validation: Not allowed to create with id')
		r = requests.delete(URL+"projects/"+pid1)
		r = requests.delete(URL+"projects/"+pid2)
	def test_post_id_list(self):
		projectData1 = {'title':'test_post','completed':False,'active':False,'description':'test_post'}
		projectData2 = {'title':'test_post','completed':False,'active':False,'description':'test_post'}
		addResponse = requests.post(URL+"projects",json = projectData1)
		pid1 = addResponse.json()['id']
		addResponse = requests.post(URL+"projects",json = projectData2)
		pid2 = addResponse.json()['id']
		data = [{'id':pid1},{'id':pid2}]
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = data)
		self.assertEqual(r.status_code,400)
		self.assertTrue('java.lang.IllegalStateException' in r.json()['errorMessages'][0])
		r = requests.delete(URL+"projects/"+pid1)
		r = requests.delete(URL+"projects/"+pid2)
	def test_post_with_extra_data(self):
		id = 1
		projectData = {'title':'test_post','completed':False,'active':False,'description':'test_post'}
		addResponse = requests.post(URL+"projects",json = projectData)
		pid = addResponse.json()['id']
		data = {'id':pid,'title':'aaa'}
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = data)
		projectData['id'] = pid
		projectData['tasks'] = [{'id':'1'}]
		projectData['completed'] = 'false'
		projectData['active'] = 'false'
		r = requests.get(URL+"todos/1/tasksof").json()['projects']
		self.assertTrue(projectData in r)
		r = requests.delete(URL+"todos/"+str(id)+"/tasksof/"+pid)
		r = requests.delete(URL+"projects/"+pid)
	def test_post_with_extra_non_existing_data(self):
		id = 1
		projectData = {'title':'test_post','completed':False,'active':False,'description':'test_post'}
		addResponse = requests.post(URL+"projects",json = projectData)
		pid = addResponse.json()['id']
		data = {'id':pid,'sss':'aaa'}
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'java.lang.NullPointerException')
		r = requests.delete(URL+"projects/"+pid)
	def test_post_with_non_existing_data(self):
		id = 1
		data = {'sss':'aaa'}
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'java.lang.NullPointerException')

class TodosIdTaskofIdTester(unittest.TestCase):
	def setUp(self):
		try:
			r = requests.get(URL)
		except ConnectionError as e:
			self.fail("conditions not met")
	def test_delete(self):
		id = 1
		projectData = {'title':'test_post','completed':False,'active':False,'description':'test_post'}
		addResponse = requests.post(URL+"projects",json = projectData)
		pid = addResponse.json()['id']
		data = {'id':pid}
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = data)
		projectData['id'] = pid
		projectData['tasks'] = [{'id':'1'}]
		projectData['completed'] = 'false'
		projectData['active'] = 'false'
		r = requests.get(URL+"todos/1/tasksof").json()['projects']
		self.assertTrue(projectData in r)
		r = requests.delete(URL+"todos/"+str(id)+"/tasksof/"+pid)
		result = requests.get(URL+"todos/"+str(id)+"/tasksof")
		self.assertEqual(len(result.json()['projects']),1)
		self.assertTrue(projectData not in result.json()['projects'])
		r = requests.delete(URL+"projects/"+pid)
	def test_double_delete(self):
		id = 1
		projectData = {'title':'test_post','completed':False,'active':False,'description':'test_post'}
		addResponse = requests.post(URL+"projects",json = projectData)
		pid = addResponse.json()['id']
		data = {'id':pid}
		r = requests.post(URL+"todos/"+str(id)+"/tasksof",json = data)
		projectData['id'] = pid
		projectData['tasks'] = [{'id':'1'}]
		projectData['completed'] = 'false'
		projectData['active'] = 'false'
		r = requests.get(URL+"todos/1/tasksof").json()['projects']
		self.assertTrue(projectData in r)
		r = requests.delete(URL+"todos/"+str(id)+"/tasksof/"+pid)
		result = requests.get(URL+"todos/"+str(id)+"/tasksof")
		self.assertEqual(len(result.json()['projects']),1)
		self.assertTrue(projectData not in result.json()['projects'])
		r = requests.delete(URL+"todos/"+str(id)+"/tasksof/"+pid)
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find any instances with todos/1/tasksof/'+pid)
		r = requests.delete(URL+"projects/"+pid)
	def test_delete_non_exist(self):
		id = 1
		pid = '3'
		r = requests.delete(URL+"todos/"+str(id)+"/tasksof/"+pid)
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find any instances with todos/1/tasksof/'+pid)
		
##################################

class TodosIdCategoriesTester(unittest.TestCase):
	def setUp(self):
		try:
			r = requests.get(URL)
		except ConnectionError as e:
			self.fail("conditions not met")
	def test_get(self):
		answer = requests.get(URL+"categories/1").json()
		result = requests.get(URL+"todos/1/categories").json()
		self.assertEqual(result,answer)
	def test_get_with_wrong_id(self):
		print('test_get_with_wrong_id\n')
		id = 3
		result = requests.get(URL+"todos/"+str(id)+"/categories")
		print('this is strange, it should be a error code instead of 2 copy of category information\n')
		self.assertEqual(result.status_code,200)
	def test_post(self):
		id = 1
		categoryData = {'title':'test_post','description':'test_post'}
		addResponse = requests.post(URL+"categories",json = categoryData)
		cid = addResponse.json()['id']
		data = {'id':cid}
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = data)
		categoryData['id'] = cid
		r = requests.get(URL+"todos/1/categories").json()['categories']
		self.assertTrue(categoryData in r)
		r = requests.delete(URL+"todos/"+str(id)+"/categories/"+cid)
		r = requests.delete(URL+"categories/"+cid)
	def test_post_repeat(self):
		answer = requests.get(URL+"todos/1/categories").json()
		data = {'id':'1'}
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = data)
		result = requests.get(URL+"todos/1/categories").json()
		self.assertEqual(result,answer)
	def test_post_no_data(self):
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/categories")
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'title : field is mandatory')
	def test_post_empty_data(self):
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = {})
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'title : field is mandatory')
	def test_post_non_existing_id(self):
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = {'id':'3'})
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find thing matching value for id')
	def test_post_empty_id(self):
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = {'id':''})
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find thing matching value for id')
	def test_post_space_id(self):
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = {'id':' '})
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find thing matching value for id')
	def test_post_int_id(self):
		categoryData = {'title':'test_post','description':'test_post'}
		addResponse = requests.post(URL+"categories",json = categoryData)
		cid = addResponse.json()['id']
		id = 1
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = {'id':int(cid)})
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find thing matching value for id')
		r = requests.delete(URL+"categories/"+cid)
	def test_post_id_list(self):
		id = 1
		categoryData1 = {'title':'test_post','description':'test_post'}
		categoryData2 = {'title':'test_post','description':'test_post'}
		addResponse = requests.post(URL+"categories",json = categoryData1)
		cid1 = addResponse.json()['id']
		addResponse = requests.post(URL+"categories",json = categoryData2)
		cid2 = addResponse.json()['id']
		data = {'id':[cid1,cid2]}
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'Invalid Creation: Failed Validation: Not allowed to create with id')
		r = requests.delete(URL+"categories/"+cid1)
		r = requests.delete(URL+"categories/"+cid2)
	def test_post_id_list(self):
		id = 1
		categoryData1 = {'title':'test_post','description':'test_post'}
		categoryData2 = {'title':'test_post','description':'test_post'}
		addResponse = requests.post(URL+"categories",json = categoryData1)
		cid1 = addResponse.json()['id']
		addResponse = requests.post(URL+"categories",json = categoryData2)
		cid2 = addResponse.json()['id']
		data = [{'id':cid1},{'id':cid2}]
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = data)
		self.assertEqual(r.status_code,400)
		self.assertTrue('java.lang.IllegalStateException' in r.json()['errorMessages'][0])
		r = requests.delete(URL+"categories/"+cid1)
		r = requests.delete(URL+"categories/"+cid2)
	def test_post_with_extra_data(self):
		id = 1
		categoryData = {'title':'test_post','description':'test_post'}
		addResponse = requests.post(URL+"categories",json = categoryData)
		cid = addResponse.json()['id']
		data = {'id':cid,'title':'aaa'}
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = data)
		categoryData['id'] = cid
		r = requests.get(URL+"todos/1/categories").json()['categories']
		self.assertTrue(categoryData in r)
		r = requests.delete(URL+"todos/"+str(id)+"/categories/"+cid)
		r = requests.delete(URL+"categories/"+cid)
	def test_post_with_extra_non_existing_data(self):
		id = 1
		categoryData = {'title':'test_post','description':'test_post'}
		addResponse = requests.post(URL+"categories",json = categoryData)
		cid = addResponse.json()['id']
		data = {'id':cid,'sss':'aaa'}
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'java.lang.NullPointerException')
		r = requests.delete(URL+"categories/"+cid)
	def test_post_with_non_existing_data(self):
		id = 1
		data = {'sss':'aaa'}
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = data)
		self.assertEqual(r.status_code,400)
		self.assertEqual(r.json()['errorMessages'][0],'java.lang.NullPointerException')

class TodosIdCategoriesIdTester(unittest.TestCase):
	def setUp(self):
		try:
			r = requests.get(URL)
		except ConnectionError as e:
			self.fail("conditions not met")
	def test_delete(self):
		id = 1
		categoryData = {'title':'test_post','description':'test_post'}
		addResponse = requests.post(URL+"categories",json = categoryData)
		cid = addResponse.json()['id']
		data = {'id':cid}
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = data)
		categoryData['id'] = cid
		r = requests.get(URL+"todos/1/categories").json()['categories']
		self.assertTrue(categoryData in r)
		r = requests.delete(URL+"todos/"+str(id)+"/categories/"+cid)
		r = requests.get(URL+"todos/"+str(id)+"/categories")
		self.assertEqual(len(r.json()['categories']),1)
		self.assertTrue(categoryData not in r.json()['categories'])
		r = requests.delete(URL+"todos/"+str(id)+"/categories/"+cid)
		
		r = requests.delete(URL+"categories/"+cid)
	def test_double_delete(self):
		id = 1
		categoryData = {'title':'test_post','description':'test_post'}
		addResponse = requests.post(URL+"categories",json = categoryData)
		cid = addResponse.json()['id']
		data = {'id':cid}
		r = requests.post(URL+"todos/"+str(id)+"/categories",json = data)
		categoryData['id'] = cid
		r = requests.get(URL+"todos/1/categories").json()['categories']
		self.assertTrue(categoryData in r)
		r = requests.delete(URL+"todos/"+str(id)+"/categories/"+cid)
		r = requests.get(URL+"todos/"+str(id)+"/categories")
		self.assertEqual(len(r.json()['categories']),1)
		self.assertTrue(categoryData not in r.json()['categories'])
		r = requests.delete(URL+"todos/"+str(id)+"/categories/"+cid)
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find any instances with todos/1/categories/'+cid)
		r = requests.delete(URL+"categories/"+cid)
	def test_delete_non_exist(self):
		id = 1
		cid = '3'
		r = requests.delete(URL+"todos/"+str(id)+"/categories/"+cid)
		self.assertEqual(r.status_code,404)
		self.assertEqual(r.json()['errorMessages'][0],'Could not find any instances with todos/1/categories/'+cid)		

if __name__ == '__main__':
	unittest.main()	