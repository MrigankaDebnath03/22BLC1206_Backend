
---

# 22BLC1206_Backend

A secure REST API for user authentication, file management, and file sharing, built with Go, PostgreSQL, and Redis. Deployed on Render.

## Endpoints

### User

- **Register**  
  **POST** `/register`  
  **Request:**
  ```bash
  curl -X POST https://two2blc1206backend.onrender.com/register \
    -H "Content-Type: application/json" \
    -d '{"username":"john_doe", "email":"john@example.com", "password":"secret"}'
  ```
  **Response:**
  ```json
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2023-07-15T12:34:56Z"
  }
  ```

- **Login**  
  **POST** `/login`  
  **Request:**
  ```bash
  curl -X POST https://two2blc1206backend.onrender.com/login \
    -H "Content-Type: application/json" \
    -d '{"username":"john_doe", "password":"secret"}'
  ```
  **Response:**
  ```json
  {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_at": "2023-07-16T12:34:56Z"
  }
  ```

### File Management

- **Upload**  
  **POST** `/upload` (multipart/form-data; requires JWT)  
  **Request:**
  ```bash
  curl -X POST https://two2blc1206backend.onrender.com/upload \
    -H "Authorization: Bearer <JWT_TOKEN>" \
    -F "file=@/path/to/file.jpg" \
    -F "is_public=true"
  ```
  **Response:**
  ```json
  {
    "id": 5,
    "filename": "file.jpg",
    "status": "uploaded",
    "is_public": true
  }
  ```

- **Download**  
  **GET** `/download?id=<FILE_ID>` (requires JWT)  
  **Request:**
  ```bash
  curl -X GET https://two2blc1206backend.onrender.com/download?id=5 \
    -H "Authorization: Bearer <JWT_TOKEN>" \
    --output downloaded_file.jpg
  ```

- **List Files**  
  **GET** `/files` (requires JWT)  
  **Request:**
  ```bash
  curl -X GET https://two2blc1206backend.onrender.com/files \
    -H "Authorization: Bearer <JWT_TOKEN>"
  ```
  **Response:**
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

- **Share**  
  **POST** `/share` (requires JWT)  
  **Request:**
  ```bash
  curl -X POST https://two2blc1206backend.onrender.com/share \
    -H "Authorization: Bearer <JWT_TOKEN>" \
    -H "Content-Type: application/json" \
    -d '{"file_id":5, "shared_with":2}'
  ```
  **Response:** `201 Created`

- **Delete**  
  **DELETE** `/delete?id=<FILE_ID>` (requires JWT)  
  **Request:**
  ```bash
  curl -X DELETE https://two2blc1206backend.onrender.com/delete?id=5 \
    -H "Authorization: Bearer <JWT_TOKEN>"
  ```
  **Response:** `204 No Content`

## Local Setup

1. **Clone the Repo**
   ```bash
   git clone https://github.com/MrigankaDebnath03/22BLC1206_Backend.git
   cd 22BLC1206_Backend
   ```

2. **Configure Environment**  
   Create a `.env` file:
   ```env
   JWT_SECRET=your_secret_key
   ```

3. **Start Services**
   ```bash
   docker-compose up
   ```

4. **API Access**  
   Visit: [http://localhost:8080](http://localhost:8080)

## Deployed API

- **Base URL:**  
  `https://two2blc1206backend.onrender.com`

*Note: The first request may take ~30s due to Render's cold start.*

## Automated Testing

1. **Install Dependencies**
   ```bash
   pip install pytest requests
   ```

2. **Run Tests**
   ```bash
   python3 automated-api-test.py
   ```
   Follow the prompts to select a test file.

## Contributing

Visit our [GitHub Repository](https://github.com/MrigankaDebnath03/22BLC1206_Backend.git) to contribute or view the source code.

---
