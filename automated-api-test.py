# import pytest
# import requests
# import os
# import random
# import string
# import json
# from tkinter import Tk, filedialog

# BASE_URL = "http://localhost:8080"
# REQUEST_TIMEOUT = 15  # seconds

# def print_response(response, description=""):
#     """Helper function to print API responses"""
#     print(f"\n{'='*50}")
#     print(f"RESPONSE: {description}")
    
#     if hasattr(response, 'status_code'):  # It's a response object
#         print(f"Status Code: {response.status_code}")
#         try:
#             print("Headers:", json.dumps(dict(response.headers), indent=2))
#             if response.content:
#                 print("Body:", json.dumps(response.json(), indent=2))
#         except json.JSONDecodeError:
#             print("Body:", response.text)
#     else:  # It's a dictionary
#         print("Data:", json.dumps(response, indent=2))
#     print(f"{'='*50}\n")

# def select_file():
#     """Prompt user to select a test file"""
#     root = Tk()
#     root.withdraw()
#     file_path = filedialog.askopenfilename(title="Select a file to upload")
#     if not file_path:
#         pytest.exit("No file selected. Exiting tests.")
#     return file_path

# TEST_FILE_PATH = select_file()

# def random_string(length=10):
#     """Generate random string for test data"""
#     return ''.join(random.choices(string.ascii_lowercase, k=length))

# @pytest.fixture(scope="module")
# def test_user():
#     """Register and login a test user"""
#     username = random_string()
#     email = f"{username}@example.com"
#     password = "testpassword"

#     # Register
#     payload = {"username": username, "email": email, "password": password}
#     response = requests.post(
#         f"{BASE_URL}/register",
#         json=payload,
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(response, f"Registering user {username}")
#     assert response.status_code == 200
#     user_id = response.json()['id']

#     # Login
#     login_response = requests.post(
#         f"{BASE_URL}/login",
#         json={"username": username, "password": password},
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(login_response, f"Logging in user {username}")
#     assert login_response.status_code == 200
#     token = login_response.json()['token']

#     yield {"id": user_id, "username": username, "email": email, "token": token}

# @pytest.fixture
# def test_user_2():
#     """Register and login a second user for sharing tests"""
#     username = random_string()
#     email = f"{username}@example.com"
#     password = "testpassword"

#     # Register
#     response = requests.post(
#         f"{BASE_URL}/register",
#         json={"username": username, "email": email, "password": password},
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(response, f"Registering second user {username}")
#     assert response.status_code == 200
#     user_id = response.json()['id']

#     # Login
#     login_response = requests.post(
#         f"{BASE_URL}/login",
#         json={"username": username, "password": password},
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(login_response, f"Logging in second user {username}")
#     assert login_response.status_code == 200
#     token = login_response.json()['token']

#     return {"id": user_id, "username": username, "email": email, "token": token}

# @pytest.fixture
# def test_file(test_user):
#     """Upload a test file with progress tracking"""
#     print(f"\nUploading test file: {TEST_FILE_PATH}")
    
#     with open(TEST_FILE_PATH, "rb") as f:
#         response = requests.post(
#             f"{BASE_URL}/upload",
#             headers={"Authorization": f"Bearer {test_user['token']}"},
#             files={"file": (os.path.basename(TEST_FILE_PATH), f)},
#             data={"is_public": "true"},
#             timeout=REQUEST_TIMEOUT
#         )
#     print_response(response, "File upload response")
#     assert response.status_code == 200
#     file_data = response.json()
    
#     yield file_data
    
#     # Cleanup
#     print(f"\nCleaning up test file {file_data['id']}")
#     del_response = requests.delete(
#         f"{BASE_URL}/delete",
#         headers={"Authorization": f"Bearer {test_user['token']}"},
#         params={"id": file_data['id']},
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(del_response, "File deletion response")

# def test_register():
#     """Test user registration"""
#     username = random_string()
#     payload = {
#         "username": username,
#         "email": f"{username}@test.com",
#         "password": "pass"
#     }
#     response = requests.post(
#         f"{BASE_URL}/register",
#         json=payload,
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(response, "Registration test")
#     assert response.status_code == 200
#     assert "id" in response.json()

# def test_login(test_user):
#     """Test user login"""
#     response = requests.post(
#         f"{BASE_URL}/login",
#         json={"username": test_user['username'], "password": "testpassword"},
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(response, "Login test")
#     assert response.status_code == 200
#     assert "token" in response.json()

# def test_protected_endpoint(test_user):
#     """Test protected endpoint access"""
#     response = requests.get(
#         f"{BASE_URL}/protected",
#         headers={"Authorization": f"Bearer {test_user['token']}"},
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(response, "Protected endpoint test")
#     assert response.status_code == 200
#     assert response.json()['username'] == test_user['username']

# def test_file_upload(test_file):
#     """Test file upload results"""
#     print("\nTesting file upload results:")
#     print(f"File ID: {test_file['id']}")
#     print(f"Filename: {test_file['filename']}")
#     print(f"Status: {test_file['status']}")
#     print(f"Is Public: {test_file['is_public']}")
    
#     assert test_file['id'] > 0
#     assert test_file['status'] == "uploaded"
#     assert test_file['is_public'] is True

# def test_file_download(test_user, test_file):
#     """Test file download"""
#     print(f"\nTesting download for file {test_file['id']}")
#     response = requests.get(
#         f"{BASE_URL}/download",
#         headers={"Authorization": f"Bearer {test_user['token']}"},
#         params={"id": test_file['id']},
#         timeout=REQUEST_TIMEOUT,
#         stream=True
#     )
#     print_response(response, "File download response")
#     assert response.status_code == 200
#     assert "Content-Disposition" in response.headers
#     assert "Content-Length" in response.headers
#     assert int(response.headers['Content-Length']) > 0

# def test_unauthorized_file_access(test_file):
#     """Test unauthorized access to a file"""
#     response = requests.get(
#         f"{BASE_URL}/download",
#         params={"id": test_file['id']},
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(response, "Unauthorized access test")
#     assert response.status_code == 401

# def test_file_sharing(test_user, test_user_2, test_file):
#     """Test file sharing between users"""
#     # Share the file
#     share_payload = {
#         "file_id": test_file['id'],
#         "shared_with": test_user_2['id']
#     }
#     share_response = requests.post(
#         f"{BASE_URL}/share",
#         headers={"Authorization": f"Bearer {test_user['token']}"},
#         json=share_payload,
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(share_response, "File sharing response")
#     assert share_response.status_code == 201
    
#     # Verify shared user can access
#     download_response = requests.get(
#         f"{BASE_URL}/download",
#         headers={"Authorization": f"Bearer {test_user_2['token']}"},
#         params={"id": test_file['id']},
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(download_response, "Shared file download")
#     assert download_response.status_code == 200

# def test_list_files(test_user, test_file):
#     """Test listing files"""
#     response = requests.get(
#         f"{BASE_URL}/files",
#         headers={"Authorization": f"Bearer {test_user['token']}"},
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(response, "List files response")
#     assert response.status_code == 200
#     files = response.json()
#     assert any(f['id'] == test_file['id'] for f in files)

# def test_search_files(test_user, test_file):
#     """Test file search functionality"""
#     filename = os.path.basename(TEST_FILE_PATH)
#     response = requests.get(
#         f"{BASE_URL}/search",
#         headers={"Authorization": f"Bearer {test_user['token']}"},
#         params={"name": filename[:4]},  # Search with first 4 chars of filename
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(response, "File search response")
#     assert response.status_code == 200
#     files = response.json()
#     assert any(f['id'] == test_file['id'] for f in files)

# def test_invalid_file_download(test_user):
#     """Test download of a non-existing file"""
#     response = requests.get(
#         f"{BASE_URL}/download",
#         headers={"Authorization": f"Bearer {test_user['token']}"},
#         params={"id": "999999"},  # Non-existent ID
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(response, "Invalid file download test")
#     assert response.status_code == 404

# def test_file_deletion(test_user):
#     """Test file upload and deletion workflow"""
#     # Upload a new file for this test
#     with open(TEST_FILE_PATH, "rb") as f:
#         upload_response = requests.post(
#             f"{BASE_URL}/upload",
#             headers={"Authorization": f"Bearer {test_user['token']}"},
#             files={"file": (os.path.basename(TEST_FILE_PATH), f)},
#             timeout=REQUEST_TIMEOUT
#         )
#     print_response(upload_response, "Upload for deletion test")
#     assert upload_response.status_code == 200
#     file_data = upload_response.json()
    
#     # Delete the file
#     del_response = requests.delete(
#         f"{BASE_URL}/delete",
#         headers={"Authorization": f"Bearer {test_user['token']}"},
#         params={"id": file_data['id']},
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(del_response, "File deletion test")
#     assert del_response.status_code == 204
    
#     # Verify file is gone
#     verify_response = requests.get(
#         f"{BASE_URL}/download",
#         headers={"Authorization": f"Bearer {test_user['token']}"},
#         params={"id": file_data['id']},
#         timeout=REQUEST_TIMEOUT
#     )
#     print_response(verify_response, "Verify deletion test")
#     assert verify_response.status_code == 404

# if __name__ == "__main__":
#     pytest.main(['-v', '--log-level=DEBUG', __file__])

import pytest
import requests
import os
import random
import string
import json
from tkinter import Tk, filedialog

BASE_URL = "http://localhost:8080"
REQUEST_TIMEOUT = 15  # seconds

# Force print to always flush output to ensure it's not buffered
def custom_print(*args, **kwargs):
    kwargs['flush'] = True
    print(*args, **kwargs)

def print_response(response, description=""):
    """Helper function to print API responses"""
    custom_print(f"\n{'='*50}")
    custom_print(f"RESPONSE: {description}")
    
    if hasattr(response, 'status_code'):  # It's a response object
        custom_print(f"Status Code: {response.status_code}")
        custom_print("Headers:", json.dumps(dict(response.headers), indent=2))
        
        # Always try to print the response body
        try:
            if response.content:
                try:
                    json_response = response.json()
                    custom_print("JSON Body:", json.dumps(json_response, indent=2))
                except json.JSONDecodeError:
                    custom_print("Text Body:", response.text)
            else:
                custom_print("Empty response body")
        except Exception as e:
            custom_print(f"Error parsing response: {str(e)}")
            custom_print("Raw content:", response.content)
    else:  # It's a dictionary
        custom_print("Data:", json.dumps(response, indent=2))
    custom_print(f"{'='*50}\n")

def select_file():
    """Prompt user to select a test file"""
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a file to upload")
    if not file_path:
        pytest.exit("No file selected. Exiting tests.")
    return file_path

TEST_FILE_PATH = select_file()

def random_string(length=10):
    """Generate random string for test data"""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

@pytest.fixture(scope="module")
def test_user():
    """Register and login a test user"""
    username = random_string()
    email = f"{username}@example.com"
    password = "testpassword"

    # Register
    payload = {"username": username, "email": email, "password": password}
    response = requests.post(
        f"{BASE_URL}/register",
        json=payload,
        timeout=REQUEST_TIMEOUT
    )
    print_response(response, f"Registering user {username}")
    assert response.status_code == 200
    user_id = response.json()['id']

    # Login
    login_response = requests.post(
        f"{BASE_URL}/login",
        json={"username": username, "password": password},
        timeout=REQUEST_TIMEOUT
    )
    print_response(login_response, f"Logging in user {username}")
    assert login_response.status_code == 200
    token = login_response.json()['token']

    yield {"id": user_id, "username": username, "email": email, "token": token}

@pytest.fixture
def test_user_2():
    """Register and login a second user for sharing tests"""
    username = random_string()
    email = f"{username}@example.com"
    password = "testpassword"

    # Register
    response = requests.post(
        f"{BASE_URL}/register",
        json={"username": username, "email": email, "password": password},
        timeout=REQUEST_TIMEOUT
    )
    print_response(response, f"Registering second user {username}")
    assert response.status_code == 200
    user_id = response.json()['id']

    # Login
    login_response = requests.post(
        f"{BASE_URL}/login",
        json={"username": username, "password": password},
        timeout=REQUEST_TIMEOUT
    )
    print_response(login_response, f"Logging in second user {username}")
    assert login_response.status_code == 200
    token = login_response.json()['token']

    return {"id": user_id, "username": username, "email": email, "token": token}

@pytest.fixture
def test_file(test_user):
    """Upload a test file with progress tracking"""
    custom_print(f"\nUploading test file: {TEST_FILE_PATH}")
    
    with open(TEST_FILE_PATH, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/upload",
            headers={"Authorization": f"Bearer {test_user['token']}"},
            files={"file": (os.path.basename(TEST_FILE_PATH), f)},
            data={"is_public": "true"},
            timeout=REQUEST_TIMEOUT
        )
    print_response(response, "File upload response")
    assert response.status_code == 200
    file_data = response.json()
    
    yield file_data
    
    # Cleanup
    custom_print(f"\nCleaning up test file {file_data['id']}")
    del_response = requests.delete(
        f"{BASE_URL}/delete",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        params={"id": file_data['id']},
        timeout=REQUEST_TIMEOUT
    )
    print_response(del_response, "File deletion response")

def test_register():
    """Test user registration"""
    username = random_string()
    payload = {
        "username": username,
        "email": f"{username}@test.com",
        "password": "pass"
    }
    custom_print(f"\nTesting registration with username: {username}")
    response = requests.post(
        f"{BASE_URL}/register",
        json=payload,
        timeout=REQUEST_TIMEOUT
    )
    print_response(response, "Registration test")
    assert response.status_code == 200
    assert "id" in response.json()

def test_login(test_user):
    """Test user login"""
    custom_print(f"\nTesting login for user: {test_user['username']}")
    response = requests.post(
        f"{BASE_URL}/login",
        json={"username": test_user['username'], "password": "testpassword"},
        timeout=REQUEST_TIMEOUT
    )
    print_response(response, "Login test")
    assert response.status_code == 200
    assert "token" in response.json()

def test_protected_endpoint(test_user):
    """Test protected endpoint access"""
    custom_print(f"\nTesting protected endpoint for user: {test_user['username']}")
    response = requests.get(
        f"{BASE_URL}/protected",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        timeout=REQUEST_TIMEOUT
    )
    print_response(response, "Protected endpoint test")
    assert response.status_code == 200
    assert response.json()['username'] == test_user['username']

def test_file_upload(test_file):
    """Test file upload results"""
    custom_print("\nTesting file upload results:")
    custom_print(f"File ID: {test_file['id']}")
    custom_print(f"Filename: {test_file['filename']}")
    custom_print(f"Status: {test_file['status']}")
    custom_print(f"Is Public: {test_file['is_public']}")
    
    # Print the full file data as JSON
    custom_print("Complete file data:", json.dumps(test_file, indent=2))
    
    assert test_file['id'] > 0
    assert test_file['status'] == "uploaded"
    assert test_file['is_public'] is True

def test_file_download(test_user, test_file):
    """Test file download"""
    custom_print(f"\nTesting download for file {test_file['id']}")
    response = requests.get(
        f"{BASE_URL}/download",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        params={"id": test_file['id']},
        timeout=REQUEST_TIMEOUT,
        stream=True
    )
    print_response(response, "File download response")
    assert response.status_code == 200
    assert "Content-Disposition" in response.headers
    assert "Content-Length" in response.headers
    assert int(response.headers['Content-Length']) > 0

def test_unauthorized_file_access(test_file):
    """Test unauthorized access to a file"""
    custom_print(f"\nTesting unauthorized access to file {test_file['id']}")
    response = requests.get(
        f"{BASE_URL}/download",
        params={"id": test_file['id']},
        timeout=REQUEST_TIMEOUT
    )
    print_response(response, "Unauthorized access test")
    assert response.status_code == 401

def test_file_sharing(test_user, test_user_2, test_file):
    """Test file sharing between users"""
    # Share the file
    share_payload = {
        "file_id": test_file['id'],
        "shared_with": test_user_2['id']
    }
    custom_print(f"\nSharing file {test_file['id']} with user {test_user_2['username']}")
    share_response = requests.post(
        f"{BASE_URL}/share",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json=share_payload,
        timeout=REQUEST_TIMEOUT
    )
    print_response(share_response, "File sharing response")
    assert share_response.status_code == 201
    
    # Verify shared user can access
    custom_print(f"\nVerifying shared user {test_user_2['username']} can access file {test_file['id']}")
    download_response = requests.get(
        f"{BASE_URL}/download",
        headers={"Authorization": f"Bearer {test_user_2['token']}"},
        params={"id": test_file['id']},
        timeout=REQUEST_TIMEOUT
    )
    print_response(download_response, "Shared file download")
    assert download_response.status_code == 200

def test_list_files(test_user, test_file):
    """Test listing files"""
    custom_print(f"\nListing files for user: {test_user['username']}")
    response = requests.get(
        f"{BASE_URL}/files",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        timeout=REQUEST_TIMEOUT
    )
    print_response(response, "List files response")
    assert response.status_code == 200
    files = response.json()
    custom_print(f"Found {len(files)} files")
    assert any(f['id'] == test_file['id'] for f in files)

def test_search_files(test_user, test_file):
    """Test file search functionality"""
    filename = os.path.basename(TEST_FILE_PATH)
    search_term = filename[:4]  # Search with first 4 chars of filename
    custom_print(f"\nSearching files with term: {search_term}")
    response = requests.get(
        f"{BASE_URL}/search",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        params={"name": search_term},
        timeout=REQUEST_TIMEOUT
    )
    print_response(response, "File search response")
    assert response.status_code == 200
    files = response.json()
    custom_print(f"Search returned {len(files)} files")
    assert any(f['id'] == test_file['id'] for f in files)

def test_invalid_file_download(test_user):
    """Test download of a non-existing file"""
    invalid_id = 999999
    custom_print(f"\nTesting download of non-existent file ID: {invalid_id}")
    response = requests.get(
        f"{BASE_URL}/download",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        params={"id": str(invalid_id)},
        timeout=REQUEST_TIMEOUT
    )
    print_response(response, "Invalid file download test")
    assert response.status_code == 404

def test_file_deletion(test_user):
    """Test file upload and deletion workflow"""
    # Upload a new file for this test
    custom_print(f"\nUploading test file for deletion test: {TEST_FILE_PATH}")
    with open(TEST_FILE_PATH, "rb") as f:
        upload_response = requests.post(
            f"{BASE_URL}/upload",
            headers={"Authorization": f"Bearer {test_user['token']}"},
            files={"file": (os.path.basename(TEST_FILE_PATH), f)},
            timeout=REQUEST_TIMEOUT
        )
    print_response(upload_response, "Upload for deletion test")
    assert upload_response.status_code == 200
    file_data = upload_response.json()
    
    # Delete the file
    custom_print(f"\nDeleting file: {file_data['id']}")
    del_response = requests.delete(
        f"{BASE_URL}/delete",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        params={"id": file_data['id']},
        timeout=REQUEST_TIMEOUT
    )
    print_response(del_response, "File deletion test")
    assert del_response.status_code == 204
    
    # Verify file is gone
    custom_print(f"\nVerifying file {file_data['id']} is deleted")
    verify_response = requests.get(
        f"{BASE_URL}/download",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        params={"id": file_data['id']},
        timeout=REQUEST_TIMEOUT
    )
    print_response(verify_response, "Verify deletion test")
    assert verify_response.status_code == 404

if __name__ == "__main__":
    pytest.main(['-v', '--no-header', __file__])