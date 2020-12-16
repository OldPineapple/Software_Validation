import requests
import json
import unittest
import os
from threading import Thread

def run_server():
    os.system("java -jar runTodoManagerRestAPI-1.5.5.jar")
    
class TestProjects(unittest.TestCase):
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
    
         
    def test_get_projects(self):
         response = requests.get("http://localhost:4567/projects")
         response_body = response.json()
         assert response_body["projects"][0]["id"] == "1"
         assert response_body["projects"][0]["title"] == "Office Work"
         assert response_body["projects"][0]["completed"] == "false"
         assert response_body["projects"][0]["active"] == "false"
         assert response_body["projects"][0]["description"] == ""
         assert len(response_body["projects"][0]["tasks"]) == 2
    
    def test_delete_projects_withID(self):
        response = requests.post("http://localhost:4567/projects")
        response = requests.get("http://localhost:4567/projects")
        response_body = response.json()
        origin = len(response_body["projects"])
        response1 = requests.delete("http://localhost:4567/projects/2")
        response2 = requests.get("http://localhost:4567/projects")
        response_body2 = response2.json()
        assert len(response_body2["projects"]) == origin-1

    def test_post_projects_withID_categories(self):
        url = "http://localhost:4567/projects/1/categories"
        headers = {'Content-Type': 'application/json' }
        category={"id":"1"}
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        response2 = requests.get("http://localhost:4567/projects/1/categories")
        response_body2 = response2.json()
        assert response_body2["categories"][0]["id"] == "1"
        assert response_body2["categories"][0]["title"] == "Office"
        assert response_body2["categories"][0]["description"] == ""
    def test_post_projects(self):
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json' }
        project={"title": "School Work", "completed": False, "active": False,"description": "good"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response2 = requests.get("http://localhost:4567/projects/2")
        response_body1 = response1.json()
        response_body2 = response2.json()
        assert response_body2["projects"][0]["id"] == response_body1["id"]
        assert response_body2["projects"][0]["title"] == "School Work"
        assert response_body2["projects"][0]["completed"] == "false"
        assert response_body2["projects"][0]["active"] == "false"
        assert response_body2["projects"][0]["description"] == "good"	
    def test_head_projects(self):
        response = requests.head("http://localhost:4567/projects")
        assert response.headers["Content-Type"] == "application/json"
        assert response.headers["Transfer-Encoding"] == "chunked"

        
    def test_get_projects_withID(self):
         response = requests.get("http://localhost:4567/projects/1")
         response_body = response.json()
         assert response_body["projects"][0]["id"] =="1"
         assert response_body["projects"][0]["title"] == "Office Work"
         assert response_body["projects"][0]["completed"] == "false"
         assert response_body["projects"][0]["active"] == "false"
         assert response_body["projects"][0]["description"] == ""
         assert len(response_body["projects"][0]["tasks"])==2
         
    def test_head_projects_withID(self):
        response = requests.head("http://localhost:4567/projects/2")
        assert response.headers["Content-Type"] == "application/json"
        assert response.headers["Transfer-Encoding"] == "chunked"
        
    def test_post_projects_withID(self):
        url = "http://localhost:4567/projects/1"
        headers = {'Content-Type': 'application/json' }
        project={"title": "School Work", "completed": False, "active": False,"description": "good"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response2 = requests.get("http://localhost:4567/projects/1")
        response_body1 = response1.json()
        response_body2 = response2.json()
        assert response_body2["projects"][0]["id"] == "1"
        assert response_body2["projects"][0]["title"] == "School Work"
        assert response_body2["projects"][0]["completed"] == "false"
        assert response_body2["projects"][0]["active"] == "false"
        assert response_body2["projects"][0]["description"] == "good"
    def test_put_projects_withID(self):
        url = "http://localhost:4567/projects/1"
        headers = {'Content-Type': 'application/json' }
        project={"title": "Outside", "completed": True, "active": True,"description": "not good"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response2 = requests.get("http://localhost:4567/projects/1")
        response_body1 = response1.json()
        response_body2 = response2.json()
        assert response_body2["projects"][0]["id"] == "1"
        assert response_body2["projects"][0]["title"] == "Outside"
        assert response_body2["projects"][0]["completed"] == "true"
        assert response_body2["projects"][0]["active"] == "true"
        assert response_body2["projects"][0]["description"] == "not good"

    def test_post_projects_withID_tasks(self):
        response = requests.delete("http://localhost:4567/projects/1/tasks/1")
        response = requests.get("http://localhost:4567/projects/1/tasks")
        response_body = response.json()
        assert len(response_body["todos"])== 1
        url = "http://localhost:4567/projects/1/tasks"
        headers = {'Content-Type': 'application/json' }
        todo={"id":"1"}
        response1 = requests.post(url, headers=headers, data=json.dumps(todo))
        response2 = requests.get("http://localhost:4567/projects/1/tasks")
        response_body2 = response2.json()
        assert len(response_body2["todos"])==2
    def test_head_projects_withID_categories(self):
        response = requests.head("http://localhost:4567/projects/1/categories")
        assert response.headers["Content-Type"] == "application/json"
        assert response.headers["Transfer-Encoding"] == "chunked"

    def test_get_projects_withID_categories(self):
        response1 = requests.post("http://localhost:4567/projects/1/categories",json={'id':'1'})
        response2 = requests.get("http://localhost:4567/projects/1/categories")
        response_body2 = response2.json()
        assert response_body2["categories"][0]["id"] == "1"
        assert response_body2["categories"][0]["title"] == "Office"
        assert response_body2["categories"][0]["description"] == ""

    def test_delete_projects_withID_categories_withID(self):
        response = requests.post("http://localhost:4567/projects/1/categories",json={'id':'1'})
        response = requests.get("http://localhost:4567/projects/1/categories")
        response_body = response.json()
        origin = len(response_body["categories"])
        response1 = requests.delete("http://localhost:4567/projects/1/categories/1")
        response2 = requests.get("http://localhost:4567/projects/1/categories")
        response_body2 = response2.json()
        assert len(response_body2["categories"]) == origin-1
        

    def test_get_projects_withID_tasks(self):
        response = requests.get("http://localhost:4567/projects/1/tasks")
        response_body = response.json()
        '''
        assert response_body["todos"][0]["id"] == "2"
        assert response_body["todos"][0]["title"] ==  "file paperwork"
        assert response_body["todos"][0]["doneStatus"] == "false"
        assert response_body["todos"][0]["description"] == ""
        assert response_body["todos"][0]["tasksof"][0]["id"] == "1"
        '''
        assert len(response_body["todos"]) ==2

    def test_head_projects_withID_tasks(self):
        response = requests.head("http://localhost:4567/projects/1/tasks")
        assert response.headers["Content-Type"] == "application/json"
        assert response.headers["Transfer-Encoding"] == "chunked"
    def test_delete_projects_withID_tasks_withID(self):
        response = requests.get("http://localhost:4567/projects/1/tasks")
        response_body = response.json()
        origin = len(response_body["todos"])
        response1 = requests.delete("http://localhost:4567/projects/1/tasks/1")
        response2 = requests.get("http://localhost:4567/projects/1/tasks")
        response_body2 = response2.json()
        assert len(response_body2["todos"]) == origin-1  	
    def test_check_status_code_equals_200(self):
         response = requests.get("http://localhost:4567/projects")
         self.assertEqual(response.status_code,200)
         
    def test_check_content_type_equals_json(self):
         response = requests.get("http://localhost:4567/projects")
         self.assertEqual(response.headers["Content-Type"],"application/json")
        
        
class TestProjectsWithError(unittest.TestCase):

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
            
    def test_check_status_code_equals_200(self):
         response = requests.get("http://localhost:4567/projects")
         assert response.status_code == 200
         
    def test_check_content_type_equals_json(self):
         response = requests.get("http://localhost:4567/projects")
         assert response.headers["Content-Type"] == "application/json"
         
    def test_post_projects_withID_error(self):
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json' }
        project={"id":"3","title": "School Work", "completed": False, "active": False,"description": "good"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        assert response_body1["errorMessages"][0] =="Invalid Creation: Failed Validation: Not allowed to create with id"
        
    def test_get_projects_withID_not_exist(self):
        response = requests.get("http://localhost:4567/projects/10")
        response_body = response.json()
        assert response_body["errorMessages"][0] =="Could not find an instance with projects/10"
        
    def test_post_projects_withID_not_exist(self):
        url = "http://localhost:4567/projects/10"
        headers = {'Content-Type': 'application/json' }
        project={"title": "School Work", "completed": False, "active": False,"description": "good"}
        response = requests.post(url, headers=headers, data=json.dumps(project))
        response_body = response.json()
        assert response_body["errorMessages"][0] =="No such project entity instance with GUID or ID 10 found"

    def test_put_projects_withID_not_exist(self):
        url = "http://localhost:4567/projects/10"
        headers = {'Content-Type': 'application/json' }
        project={"title": "School Work", "completed": False, "active": False,"description": "good"}
        response = requests.put(url, headers=headers, data=json.dumps(project))
        response_body = response.json()
        assert response_body["errorMessages"][0] =="Invalid GUID for 10 entity project"

    def test_delete_projects_withID_not_exist(self):
        response = requests.delete("http://localhost:4567/projects/10")
        response_body = response.json()
        assert response_body["errorMessages"][0] =="Could not find any instances with projects/10"

    def test_get_projects_withID_not_exist_categories(self):
        response = requests.get("http://localhost:4567/projects/10/categories")
        response_body = response.json()
        assert response_body["categories"] ==[]
        
    def test_post_projects_withID_not_exist_categories(self):
        url = "http://localhost:4567/projects/10/categories"
        headers = {'Content-Type': 'application/json' }
        category={"id":"1"}
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        response_body1 = response1.json()
        assert response_body1["errorMessages"][0] =="Could not find parent thing for relationship projects/10/categories"

    def test_post_projects_withID_categories_not_exist(self):
        url = "http://localhost:4567/projects/1/categories"
        headers = {'Content-Type': 'application/json' }
        category={"id":"10"}
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        response_body1 = response1.json()
        assert response_body1["errorMessages"][0] =="Could not find thing matching value for id"
        
    def test_delete_projects_withID_not_exist_categories_withID(self):
        response = requests.delete("http://localhost:4567/projects/10/categories/1")
        response_body = response.json()
        assert response_body["errorMessages"][0] =="Could not find any instances with projects/10/categories/1"
        
    def test_delete_projects_withID_categories_withID_not_exist(self):
        response = requests.delete("http://localhost:4567/projects/1/categories/10")
        response_body = response.json()
        assert response_body["errorMessages"][0] =="Could not find any instances with projects/1/categories/10"

    def test_delete_projects_withID_not_exist_tasks_withid(self):
        response = requests.delete("http://localhost:4567/projects/9/tasks/1")
        response_body = response.json()
        assert response_body["errorMessages"][0] =="java.lang.NullPointerException"
        
    def test_post_projects_withID_not_exist_tasks_withid(self):
        url = "http://localhost:4567/projects/10/tasks"
        headers = {'Content-Type': 'application/json' }
        project={"id":"1"}
        response = requests.post(url, headers=headers, data=json.dumps(project))
        response_body = response.json()
        assert response_body["errorMessages"][0] =="Could not find parent thing for relationship projects/10/tasks"

    def test_post_projects_withID_not_exist_tasks_withid(self):
        url = "http://localhost:4567/projects/1/tasks"
        headers = {'Content-Type': 'application/json' }
        project={"id":"10"}
        response = requests.post(url, headers=headers, data=json.dumps(project))
        response_body = response.json()
        assert response_body["errorMessages"][0] =="Could not find thing matching value for id"

        
if __name__ == '__main__':
    unittest.main()
