import requests
import json
import unittest
import os
import populate_projects
import time
from datetime import datetime
from threading import Thread 

# global variables
t1_start = 0
t2 = 0
project_id = ' '
num = 10 # initial number of objects
title_length = 5 # length of title

# function to start the server, should run as a thread
def run_server():
    os.system("java -jar runTodoManagerRestAPI-1.5.5.jar")

# function to close the server
def close_server():
    try:
        requests.get('http://localhost:4567/shutdown')
    except:
        print("Closing server...")

class TestAddTodo(unittest.TestCase):

    # Before every test...
    def setUp(self):
        print("Starting Server...")
        t = Thread(target = run_server)
        t.start()
        # check if server is running
        try:
            r = requests.get('http://localhost:4567/docs')
        except:
            print("Server not running.")
        else:
            print("Server is running.")
        global t1_start
        t1_start = time.time()
        populate_projects.populate_projects(num, title_length)
        print("------------------------")
        print("Number of objects =", num)

    # After every test...
    def tearDown(self):
        # delete tha added object
        delete_response = requests.delete('http://localhost:4567/projects/' + project_id)
        t1 = time.time() - t1_start
        now = datetime.now()
        print("T1 =", t1, "T2 =", t2, "Current time =", now)
        print("------------------------")
        # close the server
        close_server()
        print("Server closed.")

    def test_add_1(self):
        global project_id
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        post_response = requests.post('http://localhost:4567/projects', json=item)
        t2 = time.time() - t2_start
        parsed = json.loads(post_response.text)
        project_id = parsed['id']
        get_response = requests.get('http://localhost:4567/projects/' + str(project_id))
        #print(get_response.text)
        get_parsed = json.loads(get_response.text)
        self.assertEqual(project_id, get_parsed['projects'][0]['id'])
        num = 100 # number of objects for the next unit test case

    def test_add_2(self):
        global project_id
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        post_response = requests.post('http://localhost:4567/projects', json=item)
        t2 = time.time() - t2_start
        parsed = json.loads(post_response.text)
        project_id = parsed['id']
        get_response = requests.get('http://localhost:4567/projects/' + str(project_id))
        #print(get_response.text)
        get_parsed = json.loads(get_response.text)
        self.assertEqual(project_id, get_parsed['projects'][0]['id'])
        num = 1000 # number of objects for the next unit test case

    def test_add_3(self):
        global project_id
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        post_response = requests.post('http://localhost:4567/projects', json=item)
        t2 = time.time() - t2_start
        parsed = json.loads(post_response.text)
        project_id = parsed['id']
        get_response = requests.get('http://localhost:4567/projects/' + str(project_id))
        #print(get_response.text)
        get_parsed = json.loads(get_response.text)
        self.assertEqual(project_id, get_parsed['projects'][0]['id'])
        num = 5000 # number of objects for the next unit test case

    def test_add_4(self):
        global project_id
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        post_response = requests.post('http://localhost:4567/projects', json=item)
        t2 = time.time() - t2_start
        parsed = json.loads(post_response.text)
        project_id = parsed['id']
        get_response = requests.get('http://localhost:4567/projects/' + str(project_id))
        #print(get_response.text)
        get_parsed = json.loads(get_response.text)
        self.assertEqual(project_id, get_parsed['projects'][0]['id'])
        num = 10000 # number of objects for the next unit test case

    def test_add_5(self):
        global project_id
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        post_response = requests.post('http://localhost:4567/projects', json=item)
        t2 = time.time() - t2_start
        parsed = json.loads(post_response.text)
        project_id = parsed['id']
        get_response = requests.get('http://localhost:4567/projects/' + str(project_id))
        #print(get_response.text)
        get_parsed = json.loads(get_response.text)
        self.assertEqual(project_id, get_parsed['projects'][0]['id'])
        num = 9000 # number of objects for the next unit test case

if __name__ == '__main__':
    # run the test
    unittest.main()
    
  
    