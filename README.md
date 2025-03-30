```markdown
# 22BLC1206_Backend

A secure REST API for user authentication, file management, and file sharing, built with Go, PostgreSQL, and Redis. Deployed on Render.

## Endpoints

### User Endpoints

- **Register**  
  **POST** `/register`  
  **Request Example:**
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
  **Request Example:**
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

### File Management Endpoints

- **Upload File**  
  **POST** `/upload` (multipart/form-data; requires JWT)  
  **Request Example:**
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

- **Download File**  
  **GET** `/download?id=<FILE_ID>` (requires JWT)  
  **Request Example:**
  ```bash
  curl -X GET https://two2blc1206backend.onrender.com/download?id=5 \
    -H "Authorization: Bearer <JWT_TOKEN>" \
    --output downloaded_file.jpg
  ```

- **List Files**  
  **GET** `/files` (requires JWT)  
  **Request Example:**
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

- **Share File**  
  **POST** `/share` (requires JWT)  
  **Request Example:**
  ```bash
  curl -X POST https://two2blc1206backend.onrender.com/share \
    -H "Authorization: Bearer <JWT_TOKEN>" \
    -H "Content-Type: application/json" \
    -d '{"file_id":5, "shared_with":2}'
  ```
  **Response:** `201 Created`

- **Delete File**  
  **DELETE** `/delete?id=<FILE_ID>` (requires JWT)  
  **Request Example:**
  ```bash
  curl -X DELETE https://two2blc1206backend.onrender.com/delete?id=5 \
    -H "Authorization: Bearer <JWT_TOKEN>"
  ```
  **Response:** `204 No Content`

## API Usage Examples for Deployed API

- **User Registration:**
  ```bash
  curl -X POST https://two2blc1206backend.onrender.com/register \
    -H "Content-Type: application/json" \
    -d '{"username":"alice", "email":"alice@example.com", "password":"mypassword"}'
  ```

- **User Login:**
  ```bash
  curl -X POST https://two2blc1206backend.onrender.com/login \
    -H "Content-Type: application/json" \
    -d '{"username":"alice", "password":"mypassword"}'
  ```

- **File Upload:**
  ```bash
  curl -X POST https://two2blc1206backend.onrender.com/upload \
    -H "Authorization: Bearer <JWT_TOKEN>" \
    -F "file=@/local/path/to/photo.png" \
    -F "is_public=true"
  ```

- **File Download:**
  ```bash
  curl -X GET https://two2blc1206backend.onrender.com/download?id=5 \
    -H "Authorization: Bearer <JWT_TOKEN>" \
    --output myphoto.png
  ```

## Local Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/MrigankaDebnath03/22BLC1206_Backend.git
   cd 22BLC1206_Backend
   ```

2. **Set Environment Variables**  
   Create a `.env` file:
   ```env
   JWT_SECRET=your_secret_key
   ```

3. **Start Services with Docker**
   ```bash
   docker-compose up
   ```

4. **Access Local API**  
   The API is available at: [http://localhost:8080](http://localhost:8080)

## Deployed API

- **Base URL:**  
  `https://two2blc1206backend.onrender.com`

*Note: The first request may take ~30s due to Render's cold start.*

## Testing

### Postman Testing

- **Setup:**
  1. Create a new Postman collection.
  2. Add requests for each endpoint using the deployed base URL.
  3. Create an environment in Postman with the following variables:
     - `base_url`: `https://two2blc1206backend.onrender.com`
     - `jwt_token`: (your JWT token obtained after login)
  4. Use the provided request examples as templates.
  5. Send requests to verify responses.

### Automated Testing

1. **Install Dependencies**
   ```bash
   pip install pytest requests
   ```

2. **Run Automated Tests**
   ```bash
   pytest automated-api-test.py -v --log-level=DEBUG
   ```
   This command runs the end-to-end tests with verbose output and debug-level logging, and performs automatic cleanup after testing.

## Contributing

Contributions are welcome! Check out our [GitHub Repository](https://github.com/MrigankaDebnath03/22BLC1206_Backend.git) for more details.
```
