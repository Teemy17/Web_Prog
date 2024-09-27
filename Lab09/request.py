import requests

url = 'http://161.246.5.62:11111/students/html'


def get_request():
    response = requests.get(url)
    return response.text

def get_each_request(id):
    response = requests.get(url + "/" + id)
    return response.text

def post_request(name, surname, id):
    new_url = "http://161.246.5.62:11111/students" 
    response = requests.post(new_url + "/" + "new" + "/" + name + "/" + surname + "/" + id)
    return response.text

id = "498875753"
name = "John"
surname = "kkkkkww"
print(post_request(name, surname, id))
print(get_request())
print(get_each_request(id))