import requests
import json

# Login
login_resp = requests.post('http://localhost:8000/api/auth/login', 
                           json={'email':'testadmin@test.com','password':'admin123'})
token = login_resp.json()['access_token']

# Test list students
headers = {'Authorization': f'Bearer {token}'}
resp = requests.get('http://localhost:8000/api/admin/students', headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")

