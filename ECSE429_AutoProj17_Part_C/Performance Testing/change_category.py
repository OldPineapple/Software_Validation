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
category_id = ' '
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

class TestChangeCategory(unittest.TestCase):

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
        global category_id
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        put_response = requests.put('http://localhost:4567/categories/' + str(num), json=item)
        print(put_response.text)
        t2 = time.time() - t2_start
        get_response = requests.get('http://localhost:4567/categories/' + str(num))
        parsed = json.loads(get_response.text)
        self.assertEqual('new_title', parsed['categories'][0]['title'])
        num = 100

    def test_add_2(self):
        global category_id
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        put_response = requests.put('http://localhost:4567/categories/' + str(num), json=item)
        print(put_response.text)
        t2 = time.time() - t2_start
        get_response = requests.get('http://localhost:4567/categories/' + str(num))
        parsed = json.loads(get_response.text)
        self.assertEqual('new_title', parsed['categories'][0]['title'])
        num = 1000

    def test_add_3(self):
        global category_id
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        put_response = requests.put('http://localhost:4567/categories/' + str(num), json=item)
        print(put_response.text)
        t2 = time.time() - t2_start
        get_response = requests.get('http://localhost:4567/categories/' + str(num))
        parsed = json.loads(get_response.text)
        self.assertEqual('new_title', parsed['categories'][0]['title'])
        num = 5000

    def test_add_4(self):
        global category_id
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        put_response = requests.put('http://localhost:4567/categories/' + str(num), json=item)
        print(put_response.text)
        t2 = time.time() - t2_start
        get_response = requests.get('http://localhost:4567/categories/' + str(num))
        parsed = json.loads(get_response.text)
        self.assertEqual('new_title', parsed['categories'][0]['title'])
        num = 10000

    def test_add_5(self):
        global category_id
        global t2
        global num
        item = {
            'title': 'new_title'
        }
        t2_start = time.time()
        put_response = requests.put('http://localhost:4567/categories/' + str(num), json=item)
        print(put_response.text)
        t2 = time.time() - t2_start
        get_response = requests.get('http://localhost:4567/categories/' + str(num))
        parsed = json.loads(get_response.text)
        self.assertEqual('new_title', parsed['categories'][0]['title'])
        num = 9000

if __name__ == '__main__':
    # run the test
    unittest.main()
    
  
    