import requests

response = requests.get('http://localhost:5001/test')
print(response.text)  # Prints the response body that is returned by the server
