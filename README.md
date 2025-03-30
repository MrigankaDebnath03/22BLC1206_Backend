```markdown
# File Sharing API

A secure REST API for user authentication, file management, and sharing built with Go, PostgreSQL, and Redis. Deployed on Render.

## API Endpoints

### 1. User Registration
**POST** `/register`  
Registers a new user.

**Example Request:**
```bash
curl -X POST https://two2blc1206backend.onrender.com/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe", "email":"john@example.com", "password":"secret"}'
```

**Example Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2023-07-15T12:34:56Z"
}
```

### 2. User Login
**POST** `/login`  
Authenticates a user and returns a JWT token.

**Example Request:**
```bash
curl -X POST https://two2blc1206backend.onrender.com/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe", "password":"secret"}'
```

**Example Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2023-07-16T12:34:56Z"
}
```

### 3. File Upload
**POST** `/upload`  
Uploads a file (multipart/form-data). Requires authentication.

**Example Request:**
```bash
curl -X POST https://two2blc1206backend.onrender.com/upload \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -F "file=@/path/to/file.jpg" \
  -F "is_public=true"
```

**Example Response:**
```json
{
  "id": 5,
  "filename": "file.jpg",
  "status": "uploaded",
  "is_public": true
}
```

### 4. File Download
**GET** `/download?id=<FILE_ID>`  
Downloads a file. Checks permissions.

**Example Request:**
```bash
curl -X GET https://two2blc1206backend.onrender.com/download?id=5 \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  --output downloaded_file.jpg
```

### 5. List Files
**GET** `/files`  
Lists all accessible files for the user.

**Example Request:**
```bash
curl -X GET https://two2blc1206backend.onrender.com/files \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

**Example Response:**
```json
[
  {
    "id": 5,
    "name": "file.jpg",
    "size": 1024,
    "content_type": "image/jpeg",
    "uploaded_at": "2023-07-15T12:35:00Z",
    "is_public": true
  }
]
```

### 6. File Sharing
**POST** `/share`  
Shares a file with another user.

**Example Request:**
```bash
curl -X POST https://two2blc1206backend.onrender.com/share \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"file_id":5, "shared_with":2}'
```

**Response:** 201 Created

### 7. Delete File
**DELETE** `/delete?id=<FILE_ID>`  
Deletes a file owned by the user.

**Example Request:**
```bash
curl -X DELETE https://two2blc1206backend.onrender.com/delete?id=5 \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

**Response:** 204 No Content

## Local Setup

1. **Clone the Repository**
```bash
git clone https://github.com/MrigankaDebnath03/22BLC1206_Backend.git
cd 22BLC1206_Backend
```

2. **Set Environment Variables**  
Create `.env` file:
```env
JWT_SECRET=your_secret_key
```

3. **Start Services with Docker**
```bash
docker-compose up
```

4. **Access API**  
The API will be available at `http://localhost:8080`.

## Using Deployed API

The API is deployed at:  
**Base URL**: `https://two2blc1206backend.onrender.com`

**Usage Tips:**
- First request may take ~30s due to Render's cold start
- Use the provided endpoints with your JWT token
- Example authenticated request:
```bash
curl -X GET https://two2blc1206backend.onrender.com/files \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

## Automated Testing

The `automated-api-test.py` file performs end-to-end testing:

**Requirements:**
```bash
pip install pytest requests
```

**Run Tests:**
1. Execute the script:
```bash
python3 automated-api-test.py
```
2. Select a test file when prompted

**Features:**
- Tests all API endpoints
- Automatic cleanup
- Real-time progress reporting
- Multi-user testing

## GitHub Repository
Find source code and contribute:  
[https://github.com/MrigankaDebnath03/22BLC1206_Backend.git](https://github.com/MrigankaDebnath03/22BLC1206_Backend.git)
```
