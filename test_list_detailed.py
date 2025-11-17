import requests
import json
import traceback

try:
    # Login
    login_resp = requests.post('http://localhost:8000/api/auth/login', 
                               json={'email':'testadmin@test.com','password':'admin123'})
    print(f"Login Status: {login_resp.status_code}")
    if login_resp.status_code != 200:
        print(f"Login Error: {login_resp.text}")
        exit(1)
    
    token = login_resp.json()['access_token']
    print(f"Token obtained: {token[:20]}...")

    # Test list students
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get('http://localhost:8000/api/admin/students', headers=headers)
    print(f"\nStudents List Status: {resp.status_code}")
    print(f"Response: {resp.text}")
    
    # Test list teachers
    resp2 = requests.get('http://localhost:8000/api/admin/teachers', headers=headers)
    print(f"\nTeachers List Status: {resp2.status_code}")
    print(f"Response: {resp2.text}")
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()

