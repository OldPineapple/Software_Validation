import requests
import json
import unittest
import os
import populate_categories
import time
from datetime import datetime
from threading import Thread 

# global variables
t1_start = 0
t2 = 0
num = 10 # number of objects
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

class TestDeleteCategory(unittest.TestCase):

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
        populate_categories.populate_categories(num, title_length)
        print("------------------------")
        print("Number of objects =", num)

    # After every test...
    def tearDown(self):
        t1 = time.time() - t1_start
        now = datetime.now()
        print("T1 =", t1, "T2 =", t2, "Current time =", now)
        print("------------------------")
        # close the server
        close_server()
        print("Server closed.")

    def test_add_1(self):
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        delete_response = requests.delete('http://localhost:4567/categories/' + str(num))
        t2 = time.time() - t2_start
        print(delete_response.text)
        get_response = requests.get('http://localhost:4567/categories/' + str(num))
        parsed = json.loads(get_response.text)
        error = parsed["errorMessages"][0]
        self.assertEqual(error, "Could not find an instance with categories/" + str(num))
        num = 100 # number of objects for the next unit test case

    def test_add_2(self):
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        delete_response = requests.delete('http://localhost:4567/categories/' + str(num))
        t2 = time.time() - t2_start
        print(delete_response.text)
        get_response = requests.get('http://localhost:4567/categories/' + str(num))
        parsed = json.loads(get_response.text)
        error = parsed["errorMessages"][0]
        self.assertEqual(error, "Could not find an instance with categories/" + str(num))
        num = 1000 # number of objects for the next unit test case

    def test_add_3(self):
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        delete_response = requests.delete('http://localhost:4567/categories/' + str(num))
        t2 = time.time() - t2_start
        print(delete_response.text)
        get_response = requests.get('http://localhost:4567/categories/' + str(num))
        parsed = json.loads(get_response.text)
        error = parsed["errorMessages"][0]
        self.assertEqual(error, "Could not find an instance with categories/" + str(num))
        num = 5000 # number of objects for the next unit test case

    def test_add_4(self):
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        delete_response = requests.delete('http://localhost:4567/categories/' + str(num))
        t2 = time.time() - t2_start
        print(delete_response.text)
        get_response = requests.get('http://localhost:4567/categories/' + str(num))
        parsed = json.loads(get_response.text)
        error = parsed["errorMessages"][0]
        self.assertEqual(error, "Could not find an instance with categories/" + str(num))
        num = 10000 # number of objects for the next unit test case

    def test_add_5(self):
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        delete_response = requests.delete('http://localhost:4567/categories/' + str(num))
        t2 = time.time() - t2_start
        print(delete_response.text)
        get_response = requests.get('http://localhost:4567/categories/' + str(num))
        parsed = json.loads(get_response.text)
        error = parsed["errorMessages"][0]
        self.assertEqual(error, "Could not find an instance with categories/" + str(num))
        num = 8000 # number of objects for the next unit test case

if __name__ == '__main__':
    # run the test
    unittest.main()
    
  
    