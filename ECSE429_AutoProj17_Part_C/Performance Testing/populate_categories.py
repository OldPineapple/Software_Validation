import json
import requests
import string
import random

# method to generate random strings
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# This method assumes that the server is already running.
def populate_categories(num, text_length):
    for i in range(num):
        text = get_random_string(text_length)
        item = {
            'title': text
        }
        post_response = requests.post('http://localhost:4567/categories', json=item)
        #print(post_response.text)

if __name__ == "__main__":
    # define num = number of objects to add, text_length = length of random generated text
    num = 10
    text_length = 10
    populate_categories(num, text_length)