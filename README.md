# 22BLC1206_Backend

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)

A secure REST API for user authentication, file management, and file sharing, built with Go, PostgreSQL, and Redis. Deployed on Render.

## 📋 Features

- **User Authentication** - Register and login with JWT-based authentication
- **File Management** - Upload, download, list, and delete files
- **File Sharing** - Share files with other users
- **Security** - JWT token-based authorization

## 🚀 API Endpoints

### User Authentication

| Endpoint | Method | Description | Authorization |
|----------|--------|-------------|---------------|
| `/register` | POST | Register a new user | None |
| `/login` | POST | Login and get JWT token | None |

### File Operations

| Endpoint | Method | Description | Authorization |
|----------|--------|-------------|---------------|
| `/upload` | POST | Upload a new file | JWT |
| `/download` | GET | Download a file | JWT |
| `/files` | GET | List all user files | JWT |
| `/share` | POST | Share a file with another user | JWT |
| `/delete` | DELETE | Delete a file | JWT |

## 🌐 Deployed API

- **Base URL:** https://two2blc1206backend.onrender.com
- **Local Development URL:** http://localhost:8080

### Endpoint Examples

**Register a new user:**
```bash
curl -X POST https://two2blc1206backend.onrender.com/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe", "email":"john@example.com", "password":"secret"}'
```

**Login:**
```bash
curl -X POST https://two2blc1206backend.onrender.com/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe", "password":"secret"}'
```

**Upload a file:**
```bash
curl -X POST https://two2blc1206backend.onrender.com/upload \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -F "file=@/path/to/file.jpg" \
  -F "is_public=true"
```

**Download a file:**
```bash
curl -X GET https://two2blc1206backend.onrender.com/download?id=5 \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  --output downloaded_file.jpg
```

**List all files:**
```bash
curl -X GET https://two2blc1206backend.onrender.com/files \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

**Share a file:**
```bash
curl -X POST https://two2blc1206backend.onrender.com/share \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"file_id":5, "shared_with":2}'
```

**Delete a file:**
```bash
curl -X DELETE https://two2blc1206backend.onrender.com/delete?id=5 \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

> **Note:** The first request may take approximately 30 seconds due to Render's cold start mechanism.


## 💻 Local Development

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MrigankaDebnath03/22BLC1206_Backend.git
   cd 22BLC1206_Backend
   ```

2. **Configure environment**
   
   Create a `.env` file in the project root:
   ```env
   JWT_SECRET=your_secret_key
   ```

3. **Start the services**
   ```bash
   docker-compose up
   ```

4. **Access the API**
   
   The API will be available at http://localhost:8080

   ## 🔍 API Usage Examples
   

### User Management

**Register a new user:**
```bash
curl -X POST http://localhost:8080/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe", "email":"john@example.com", "password":"secret"}'
```

**Login:**
```bash
curl -X POST http://localhost:8080/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe", "password":"secret"}'
```

### File Management

**Upload a file:**
```bash
curl -X POST http://localhost:8080/upload \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -F "file=@/path/to/file.jpg" \
  -F "is_public=true"
```

**Download a file:**
```bash
curl -X GET http://localhost:8080/download?id=5 \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  --output downloaded_file.jpg
```

**List all files:**
```bash
curl -X GET http://localhost:8080/files \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

**Share a file:**
```bash
curl -X POST http://localhost:8080/share \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"file_id":5, "shared_with":2}'
```

**Delete a file:**
```bash
curl -X DELETE http://localhost:8080/delete?id=5 \
  -H "Authorization: Bearer <JWT_TOKEN>"
```


## 🧪 Testing

### Testing with Postman

1. Create a new Postman collection
2. Add requests for each endpoint using the deployed base URL
3. Create an environment with variables:
   - `base_url`: `https://two2blc1206backend.onrender.com` or `http://localhost:8080`
   - `jwt_token`: (JWT token obtained after login)
4. Use the provided request examples as templates
5. Send requests to verify responses

### Automated Testing

1. **Install testing dependencies**
   ```bash
   pip install pytest requests
   ```

2. **Run automated tests**
   ```bash
   pytest automated-api-test.py -v --log-level=DEBUG
   ```


## 🔗 Links

- [GitHub Repository](https://github.com/MrigankaDebnath03/22BLC1206_Backend.git)
