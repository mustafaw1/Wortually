import requests

headers = {"Authorization": "Api-Key 99b014a28dad6c539cdbaca3ff66241fc064515e"}

response = requests.get(
    "http://localhost:8000/api/recruitment/job-posts/1/", headers=headers
)
print(response.status_code)
print(response.text)
