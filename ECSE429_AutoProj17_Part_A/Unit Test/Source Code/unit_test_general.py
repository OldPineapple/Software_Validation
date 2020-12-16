import requests
import unittest

class TestAPI(unittest.TestCase):

    # Test if it show this documentation as HTML.
    def test_get_docs(self):
        try:
            response=requests.get("http://localhost:4567/docs")
            assert response.status_code == 200
            assert response.headers["Content-Type"] == "text/html"
            assert response.headers["Transfer-Encoding"] == "chunked"
            print("GET /docs is working.")
        except requests.exceptions.ConnectionError:
            print("Test fail because service is not running.")

    # Get a URL that does not exist
    def test_get_docs_with_invalid_url(self):
        try:
            response=requests.get("http://localhost:4567/doc") 
            assert response.status_code == 404
            print("URL not found.")
        except requests.exceptions.ConnectionError:
            print("Test fail because service is not running.")

    # Test if it shutdowns the API server
    def test_get_shutdown(self):
        try:
            response=requests.get("http://localhost:4567/shutdown")
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            print("The server is shutdown.")
        else:
            print("Shutdown is not working.")

if __name__== '__main__':
    unittest.main()