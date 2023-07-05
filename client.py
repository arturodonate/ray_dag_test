import requests

response = requests.post("http://localhost:8000/default", json=3)
output = response.json()
print(output)
