import requests
import json
import unittest
import os
from threading import Thread 

def run_server():
    os.system("java -jar runTodoManagerRestAPI-1.5.5.jar")

class TestCategories(unittest.TestCase):

    # Before every test...
    def setUp(self):
        print("Starting Server...")
        t = Thread(target = run_server)
        t.start()
        print("Server starts.")

    # After every test...
    def tearDown(self):
        print("Closing server...")
        try:
            requests.get('http://localhost:4567/shutdown')
        except:
            print("Server closed.")

    def test_get(self):
        get_response = requests.get('http://localhost:4567/categories')
        parsed = json.loads(get_response.text)
        print("GET response:")
        print(json.dumps(parsed, indent=4, sort_keys=False))
        category_1 = parsed["categories"][0]
        category_2 = parsed["categories"][1]
        first_exists = False
        second_exists = False
        if ((category_1["id"] == '2' and category_1["title"] == "Home") or
            (category_2["id"] == '2' and category_2["title"] == "Home")):
            first_exists = True
        if ((category_1["id"] == '1' and category_1["title"] == "Office") or
            (category_2["id"] == '1' and category_2["title"] == "Office")):
            second_exists = True
        self.assertTrue(first_exists)
        self.assertTrue(second_exists)

    def test_post(self):
        item = {
            "title": "title_Test"
        }
        post_response = requests.post('http://localhost:4567/categories', json = item)
        print(post_response.text)
        # use GET to check the new item
        get_response = requests.get('http://localhost:4567/categories')
        parsed = json.loads(get_response.text)
        category_1 = parsed["categories"][0]
        category_2 = parsed["categories"][1]
        category_3 = parsed["categories"][2]
        # if one of the categories has a matching title, then pass
        title_exists = False
        if (category_1["title"] == "title_Test" 
            or category_2["title"] == "title_Test"
            or category_3["title"] == "title_Test"):
            title_exists = True
        self.assertTrue(title_exists)

class TestCategoriesId(unittest.TestCase):

    # Before every test...
    def setUp(self):
        print("Starting Server...")
        t = Thread(target = run_server)
        t.start()
        print("Server starts.")

    # After every test...
    def tearDown(self):
        print("Closing server...")
        try:
            requests.get('http://localhost:4567/shutdown')
        except:
            print("Server closed.")

    def test_get(self):
        get_response_1 = requests.get('http://localhost:4567/categories/1')
        get_response_2 = requests.get('http://localhost:4567/categories/2')
        parsed_1 = json.loads(get_response_1.text)
        parsed_2 = json.loads(get_response_2.text)
        category_1 = parsed_1["categories"][0]
        category_2 = parsed_2["categories"][0]
        first_exists = False
        second_exists = False
        if (category_1["id"] == '1' and category_1["title"] == "Office"):
            first_exists = True
        if (category_2["id"] == '2' and category_2["title"] == "Home"):
            second_exists = True
        self.assertTrue(first_exists)
        self.assertTrue(second_exists)

    def test_post(self):
        item = {
            "title": "title_Test"
        }
        post_response = requests.post('http://localhost:4567/categories/1', json = item)
        print(post_response.text)
        # use GET to check the new item
        get_response = requests.get('http://localhost:4567/categories/1')
        parsed = json.loads(get_response.text)
        print(json.dumps(parsed, indent=4, sort_keys=False))
        category = parsed["categories"][0]
        # if one of the categories has a matching title, then pass
        title_exists = False
        if category["title"] == "title_Test":
            title_exists = True
        self.assertTrue(title_exists)

    def test_put(self):
        item = {
            "title": "title_Test"
        }
        put_response = requests.put('http://localhost:4567/categories/1', json = item)
        print(put_response.text)
        # use GET to check the new item
        get_response = requests.get('http://localhost:4567/categories/1')
        parsed = json.loads(get_response.text)
        print(json.dumps(parsed, indent=4, sort_keys=False))
        category = parsed["categories"][0]
        # if one of the categories has a matching title, then pass
        title_exists = False
        if category["title"] == "title_Test":
            title_exists = True
        self.assertTrue(title_exists)

    def test_delete(self):
        delete_response = requests.delete('http://localhost:4567/categories/1')
        # use GET to check the deleted item
        get_response = requests.get('http://localhost:4567/categories/1')
        parsed = json.loads(get_response.text)
        error = parsed["errorMessages"][0]
        self.assertEqual(error, "Could not find an instance with categories/1")

class TestCategoriesIdProjects(unittest.TestCase):

    # Before every test...
    def setUp(self):
        print("Starting Server...")
        t = Thread(target = run_server)
        t.start()
        print("Server starts.")

    # After every test...
    def tearDown(self):
        print("Closing server...")
        try:
            requests.get('http://localhost:4567/shutdown')
        except:
            print("Server closed.")

    def test_get(self):
        get_response = requests.get('http://localhost:4567/categories/1/projects')
        parsed = json.loads(get_response.text)
        print("GET response:")
        print(json.dumps(parsed, indent=4, sort_keys=False))
        project = parsed["projects"]
        self.assertEqual(project, [])

    def test_post(self):
        item = {
            "id": '1'
        }
        post_response = requests.post('http://localhost:4567/categories/2/projects', json = item)
        print(post_response.text)
        # use GET to check the new relationship
        get_response = requests.get('http://localhost:4567/categories/2/projects')
        parsed = json.loads(get_response.text)
        project = parsed["projects"][0]
        self.assertEqual(project["id"], "1")
        self.assertEqual(project["title"], "Office Work")
        self.assertEqual(project["completed"], "false")
        self.assertEqual(project["active"], "false")

class TestCategoriesIdProjectsId(unittest.TestCase):

    # Before every test...
    def setUp(self):
        print("Starting Server...")
        t = Thread(target = run_server)
        t.start()
        print("Server starts.")

    # After every test...
    def tearDown(self):
        print("Closing server...")
        try:
            requests.get('http://localhost:4567/shutdown')
        except:
            print("Server closed.")

    def test_delete(self):
        item = {
            "id": '1'
        }
        post_response = requests.post('http://localhost:4567/categories/2/projects', json = item)
        print(post_response.text)
        # use GET to check the new relationship
        get_response = requests.get('http://localhost:4567/categories/2/projects')
        parsed = json.loads(get_response.text)
        project = parsed["projects"][0]
        self.assertEqual(project["id"], "1")
        self.assertEqual(project["title"], "Office Work")
        self.assertEqual(project["completed"], "false")
        self.assertEqual(project["active"], "false")
        # delete the new relationship
        delete_response = requests.delete('http://localhost:4567/categories/2/projects/1')
        # check the existence, should be empty
        get_response = requests.get('http://localhost:4567/categories/2/projects')
        parsed = json.loads(get_response.text)
        print("GET response:")
        print(json.dumps(parsed, indent=4, sort_keys=False))
        project = parsed["projects"]
        self.assertEqual(project, [])

class TestCategoriesIdTodos(unittest.TestCase):

    # Before every test...
    def setUp(self):
        print("Starting Server...")
        t = Thread(target = run_server)
        t.start()
        print("Server starts.")

    # After every test...
    def tearDown(self):
        print("Closing server...")
        try:
            requests.get('http://localhost:4567/shutdown')
        except:
            print("Server closed.")

    def test_get(self):
        get_response = requests.get('http://localhost:4567/categories/1/todos')
        parsed = json.loads(get_response.text)
        print("GET response:")
        print(json.dumps(parsed, indent=4, sort_keys=False))
        todo = parsed["todos"]
        self.assertEqual(todo, [])

    def test_post(self):
        item = {
            "id": '2'
        }
        post_response = requests.post('http://localhost:4567/categories/2/todos', json = item)
        print(post_response.text)
        # use GET to check the new relationship
        get_response = requests.get('http://localhost:4567/categories/2/todos')
        parsed = json.loads(get_response.text)
        todo = parsed["todos"][0]
        self.assertEqual(todo["id"], "2")
        self.assertEqual(todo["title"], "file paperwork")
        self.assertEqual(todo["doneStatus"], "false")

class TestCategoriesIdTodosId(unittest.TestCase):

    # Before every test...
    def setUp(self):
        print("Starting Server...")
        t = Thread(target = run_server)
        t.start()
        print("Server starts.")

    # After every test...
    def tearDown(self):
        print("Closing server...")
        try:
            requests.get('http://localhost:4567/shutdown')
        except:
            print("Server closed.")

    def test_delete(self):
        item = {
            "id": '2'
        }
        post_response = requests.post('http://localhost:4567/categories/2/todos', json = item)
        print(post_response.text)
        # use GET to check the new relationship
        get_response = requests.get('http://localhost:4567/categories/2/todos')
        parsed = json.loads(get_response.text)
        todo = parsed["todos"][0]
        self.assertEqual(todo["id"], "2")
        self.assertEqual(todo["title"], "file paperwork")
        self.assertEqual(todo["doneStatus"], "false")
        # delete the new relationship
        delete_response = requests.delete('http://localhost:4567/categories/2/todos/2')
        # check the existence, should be empty
        get_response = requests.get('http://localhost:4567/categories/2/todos')
        parsed = json.loads(get_response.text)
        print("GET response:")
        print(json.dumps(parsed, indent=4, sort_keys=False))
        todo = parsed["todos"]
        self.assertEqual(todo, [])

if __name__ == '__main__':
    unittest.main()