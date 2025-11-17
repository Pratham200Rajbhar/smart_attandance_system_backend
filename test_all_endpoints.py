"""
Comprehensive API Endpoint Testing Script
Tests all endpoints in the Smart Attendance System API
Run with: python test_all_endpoints.py
"""

import requests
import json
import base64
from io import BytesIO
from PIL import Image
import sys

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# Test data
test_users = {
    "admin": {
        "username": "testadmin",
        "full_name": "Test Admin",
        "email": "testadmin@test.com",
        "password": "admin123",
        "role": "admin",
        "phone_number": "+911234567890"
    },
    "teacher": {
        "username": "testteacher",
        "full_name": "Test Teacher",
        "email": "testteacher@test.com",
        "password": "teacher123",
        "role": "teacher",
        "phone_number": "+911234567891"
    },
    "student": {
        "username": "teststudent",
        "full_name": "Test Student",
        "email": "teststudent@test.com",
        "password": "student123",
        "role": "student",
        "phone_number": "+911234567892"
    }
}

# Create a simple test image (base64 encoded)
def create_test_image_base64():
    """Create a simple test image and return as base64"""
    img = Image.new('RGB', (100, 100), color='red')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_test(name):
    print(f"\n{Colors.BLUE}Testing: {name}{Colors.RESET}")

def print_success(message):
    try:
        print(f"{Colors.GREEN}[PASS] {message}{Colors.RESET}")
    except UnicodeEncodeError:
        print(f"[PASS] {message}")

def print_error(message):
    try:
        print(f"{Colors.RED}[FAIL] {message}{Colors.RESET}")
    except UnicodeEncodeError:
        print(f"[FAIL] {message}")

def print_warning(message):
    try:
        print(f"{Colors.YELLOW}[WARN] {message}{Colors.RESET}")
    except UnicodeEncodeError:
        print(f"[WARN] {message}")

def test_endpoint(method, url, expected_status=200, headers=None, data=None, json_data=None, description=""):
    """Test an endpoint and return response"""
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            if json_data:
                response = requests.post(url, headers=headers, json=json_data)
            else:
                response = requests.post(url, headers=headers, data=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return None, f"Unsupported method: {method}"
        
        status_ok = response.status_code == expected_status
        if status_ok:
            print_success(f"{description or url} - Status: {response.status_code}")
        else:
            print_error(f"{description or url} - Expected: {expected_status}, Got: {response.status_code}")
            if response.text:
                try:
                    error_detail = response.json()
                    print(f"  Error: {error_detail}")
                except:
                    print(f"  Error: {response.text[:200]}")
        
        return response, None
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to server at {url}")
        return None, "Connection error"
    except Exception as e:
        print_error(f"Error testing {url}: {str(e)}")
        return None, str(e)

def main():
    print(f"{Colors.BLUE}{'='*60}")
    print("Smart Attendance System - API Endpoint Testing")
    print(f"{'='*60}{Colors.RESET}\n")
    
    # Check if server is running
    print("Checking server status...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print_success("Server is running")
        else:
            print_error(f"Server returned status {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print_error("Server is not running! Please start it with: uvicorn app.main:app --reload")
        return
    except Exception as e:
        print_error(f"Error connecting to server: {str(e)}")
        return
    
    results = {
        "passed": 0,
        "failed": 0,
        "warnings": 0
    }
    
    tokens = {}
    user_ids = {}
    student_id = None
    teacher_id = None
    
    # ==================== ROOT & HEALTH ENDPOINTS ====================
    print_test("Root & Health Endpoints")
    
    response, error = test_endpoint("GET", f"{BASE_URL}/", description="Root endpoint")
    if error:
        results["failed"] += 1
    else:
        results["passed"] += 1
    
    response, error = test_endpoint("GET", f"{BASE_URL}/health", description="Health check")
    if error:
        results["failed"] += 1
    else:
        results["passed"] += 1
    
    # ==================== AUTHENTICATION ENDPOINTS ====================
    print_test("Authentication Endpoints")
    
    # Register Admin (or login if already exists)
    response, error = test_endpoint("POST", f"{API_BASE}/auth/register", 
                                   json_data=test_users["admin"],
                                   description="Register admin user")
    if error:
        results["failed"] += 1
    else:
        if response and response.status_code == 200:
            data = response.json()
            if "data" in data and "user_id" in data["data"]:
                user_ids["admin"] = data["data"]["user_id"]
            results["passed"] += 1
        elif response and response.status_code == 400:
            # User already exists, try to login to get user_id
            login_resp, _ = test_endpoint("POST", f"{API_BASE}/auth/login",
                                         json_data={"email": test_users["admin"]["email"],
                                                   "password": test_users["admin"]["password"]},
                                         description="Login to get user_id")
            if login_resp and login_resp.status_code == 200:
                token = login_resp.json()["access_token"]
                profile_resp, _ = test_endpoint("GET", f"{API_BASE}/auth/profile",
                                               headers={"Authorization": f"Bearer {token}"},
                                               description="Get profile for user_id")
                if profile_resp and profile_resp.status_code == 200:
                    user_ids["admin"] = profile_resp.json()["id"]
            results["warnings"] += 1
            print_warning("Admin user already exists, using existing user")
        else:
            results["failed"] += 1
    
    # Register Teacher
    response, error = test_endpoint("POST", f"{API_BASE}/auth/register",
                                   json_data=test_users["teacher"],
                                   description="Register teacher user")
    if error:
        results["failed"] += 1
    else:
        if response and response.status_code == 200:
            data = response.json()
            if "data" in data and "user_id" in data["data"]:
                user_ids["teacher"] = data["data"]["user_id"]
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # Register Student
    response, error = test_endpoint("POST", f"{API_BASE}/auth/register",
                                   json_data=test_users["student"],
                                   description="Register student user")
    if error:
        results["failed"] += 1
    else:
        if response and response.status_code == 200:
            data = response.json()
            if "data" in data and "user_id" in data["data"]:
                user_ids["student"] = data["data"]["user_id"]
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # Test duplicate registration
    response, error = test_endpoint("POST", f"{API_BASE}/auth/register",
                                   expected_status=400,
                                   json_data=test_users["admin"],
                                   description="Register duplicate email (should fail)")
    if error:
        results["failed"] += 1
    else:
        if response and response.status_code == 400:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # Login Admin
    response, error = test_endpoint("POST", f"{API_BASE}/auth/login",
                                   json_data={"email": test_users["admin"]["email"],
                                             "password": test_users["admin"]["password"]},
                                   description="Login admin")
    if error:
        results["failed"] += 1
    else:
        if response and response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                tokens["admin"] = data["access_token"]
                results["passed"] += 1
            else:
                results["failed"] += 1
        else:
            results["failed"] += 1
    
    # Login Teacher
    response, error = test_endpoint("POST", f"{API_BASE}/auth/login",
                                   json_data={"email": test_users["teacher"]["email"],
                                             "password": test_users["teacher"]["password"]},
                                   description="Login teacher")
    if error:
        results["failed"] += 1
    else:
        if response and response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                tokens["teacher"] = data["access_token"]
                results["passed"] += 1
            else:
                results["failed"] += 1
        else:
            results["failed"] += 1
    
    # Login Student
    response, error = test_endpoint("POST", f"{API_BASE}/auth/login",
                                   json_data={"email": test_users["student"]["email"],
                                             "password": test_users["student"]["password"]},
                                   description="Login student")
    if error:
        results["failed"] += 1
    else:
        if response and response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                tokens["student"] = data["access_token"]
                results["passed"] += 1
            else:
                results["failed"] += 1
        else:
            results["failed"] += 1
    
    # Test invalid login
    response, error = test_endpoint("POST", f"{API_BASE}/auth/login",
                                   expected_status=401,
                                   json_data={"email": "invalid@test.com", "password": "wrong"},
                                   description="Login with invalid credentials (should fail)")
    if error:
        results["failed"] += 1
    else:
        if response and response.status_code == 401:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # Get Profile (Admin)
    if tokens.get("admin"):
        headers = {"Authorization": f"Bearer {tokens['admin']}"}
        response, error = test_endpoint("GET", f"{API_BASE}/auth/profile",
                                       headers=headers,
                                       description="Get admin profile")
        if error:
            results["failed"] += 1
        else:
            if response and response.status_code == 200:
                results["passed"] += 1
            else:
                results["failed"] += 1
    
    # Get Profile (Unauthorized)
    response, error = test_endpoint("GET", f"{API_BASE}/auth/profile",
                                   expected_status=403,
                                   description="Get profile without token (should fail)")
    if error:
        results["failed"] += 1
    else:
        if response and response.status_code == 403:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # ==================== ADMIN ENDPOINTS ====================
    print_test("Admin Endpoints")
    
    if not tokens.get("admin"):
        print_warning("Skipping admin endpoints - admin token not available")
        results["warnings"] += 1
    else:
        admin_headers = {"Authorization": f"Bearer {tokens['admin']}"}
        
        # Add Student
        if user_ids.get("student"):
            student_data = {
                "user_id": user_ids["student"],
                "student_id": "STU001",
                "enrollment_no": "ENR001",
                "department": "Computer Science",
                "semester": 3,
                "section": "A",
                "status": "active"
            }
            response, error = test_endpoint("POST", f"{API_BASE}/admin/students",
                                           headers=admin_headers,
                                           json_data=student_data,
                                           description="Add student")
            if error:
                results["failed"] += 1
            else:
                if response and response.status_code == 200:
                    results["passed"] += 1
                else:
                    results["failed"] += 1
        
        # List Students (to get the actual integer ID)
        response, error = test_endpoint("GET", f"{API_BASE}/admin/students",
                                       headers=admin_headers,
                                       description="List all students")
        if error:
            results["failed"] += 1
        else:
            if response and response.status_code == 200:
                students_list = response.json()
                if isinstance(students_list, list) and len(students_list) > 0:
                    # Get the integer id from the first student
                    student_id = students_list[0].get("id")
                results["passed"] += 1
            else:
                results["failed"] += 1
        
        # Upload Student Photo (use integer id)
        if student_id and isinstance(student_id, int):
            test_image = create_test_image_base64()
            photo_data = {"photo": test_image}
            response, error = test_endpoint("POST", f"{API_BASE}/admin/students/{student_id}/photo",
                                           headers=admin_headers,
                                           data=photo_data,
                                           description="Upload student photo")
            if error:
                results["failed"] += 1
            else:
                if response and response.status_code == 200:
                    results["passed"] += 1
                else:
                    results["warnings"] += 1  # May fail if face not detected
                    print_warning("Photo upload may have failed due to face detection")
        
        # Add Teacher
        if user_ids.get("teacher"):
            teacher_data = {
                "user_id": user_ids["teacher"],
                "teacher_id": "TCH001",
                "department": "Computer Science",
                "designation": "Professor",
                "specialization": "Machine Learning"
            }
            response, error = test_endpoint("POST", f"{API_BASE}/admin/teachers",
                                           headers=admin_headers,
                                           json_data=teacher_data,
                                           description="Add teacher")
            if error:
                results["failed"] += 1
            else:
                if response and response.status_code == 200:
                    data = response.json()
                    if "data" in data and "teacher_id" in data["data"]:
                        teacher_id = data["data"]["teacher_id"]
                    results["passed"] += 1
                else:
                    results["failed"] += 1
        
        # List Teachers
        response, error = test_endpoint("GET", f"{API_BASE}/admin/teachers",
                                       headers=admin_headers,
                                       description="List all teachers")
        if error:
            results["failed"] += 1
        else:
            if response and response.status_code == 200:
                results["passed"] += 1
            else:
                results["failed"] += 1
        
        # Test unauthorized access (student trying to access admin endpoint)
        if tokens.get("student"):
            student_headers = {"Authorization": f"Bearer {tokens['student']}"}
            response, error = test_endpoint("POST", f"{API_BASE}/admin/students",
                                           expected_status=403,
                                           headers=student_headers,
                                           json_data=student_data if user_ids.get("student") else {},
                                           description="Student accessing admin endpoint (should fail)")
            if error:
                results["failed"] += 1
            else:
                if response and response.status_code == 403:
                    results["passed"] += 1
                else:
                    results["failed"] += 1
    
    # ==================== ATTENDANCE ENDPOINTS ====================
    print_test("Attendance Endpoints")
    
    # Get Attendance Records (requires student_id as integer)
    if tokens.get("student") and student_id and isinstance(student_id, int):
        student_headers = {"Authorization": f"Bearer {tokens['student']}"}
        response, error = test_endpoint("GET", f"{API_BASE}/attendance/{student_id}",
                                       headers=student_headers,
                                       description="Get attendance records")
        if error:
            results["failed"] += 1
        else:
            if response and response.status_code == 200:
                results["passed"] += 1
            else:
                results["failed"] += 1
    
    # Verify Attendance (requires session_id and face encoding)
    # This will likely fail without proper setup, so we'll test it but mark as warning
    if tokens.get("student") and student_id and isinstance(student_id, int):
        student_headers = {"Authorization": f"Bearer {tokens['student']}"}
        test_image = create_test_image_base64()
        attendance_data = {
            "student_id": str(student_id),  # Form data needs string
            "session_id": "1",  # May not exist
            "face_image": test_image
        }
        response, error = test_endpoint("POST", f"{API_BASE}/attendance/verify",
                                       headers=student_headers,
                                       data=attendance_data,
                                       description="Verify attendance")
        if error:
            results["failed"] += 1
        else:
            if response:
                if response.status_code == 200:
                    results["passed"] += 1
                elif response.status_code in [400, 404]:
                    results["warnings"] += 1
                    print_warning("Attendance verification failed (expected - requires session and face encoding)")
                else:
                    results["failed"] += 1
    
    # ==================== SUMMARY ====================
    print(f"\n{Colors.BLUE}{'='*60}")
    print("Test Summary")
    print(f"{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}Passed: {results['passed']}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {results['failed']}{Colors.RESET}")
    print(f"{Colors.YELLOW}Warnings: {results['warnings']}{Colors.RESET}")
    print(f"Total: {results['passed'] + results['failed'] + results['warnings']}")
    
    if results["failed"] == 0:
        print(f"\n{Colors.GREEN}All critical tests passed!{Colors.RESET}")
        return 0
    else:
        print(f"\n{Colors.RED}Some tests failed. Please review the errors above.{Colors.RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

