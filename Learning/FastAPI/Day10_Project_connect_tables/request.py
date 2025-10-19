import requests

url = "http://127.0.0.1:8000/users/me/"
headers = {"Authorization": "Bearer test123"}

response = requests.get(url, headers=headers)
user = response.json()
print(user)