# Backend API Template

A production-ready FastAPI backend template with PostgreSQL database and user authentication.

## Features

- ✅ FastAPI framework
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ JWT-based authentication
- ✅ User registration and login
- ✅ Password hashing with bcrypt
- ✅ Role-based access control (Admin users)
- ✅ CORS middleware configured
- ✅ Pydantic data validation
- ✅ Environment-based configuration

## Project Structure

```
app/
├── __init__.py
├── app.py                      # Main FastAPI application
├── config.py                   # Settings and configuration
├── database.py                 # Database setup and session
├── security.py                 # JWT and password utilities
├── models/
│   ├── __init__.py
│   └── user.py                 # User database model
├── schemas/
│   ├── __init__.py
│   └── user.py                 # Pydantic schemas for validation
├── crud/
│   ├── __init__.py
│   └── user.py                 # Database queries for users
└── api/
    ├── __init__.py
    └── endpoints/
        ├── __init__.py
        ├── auth.py             # Registration and login
        └── users.py            # User management

.env.example                    # Environment variables template
requirements.txt                # Python dependencies
main.py                         # Entry point script
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate      # On macOS/Linux
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

Update `.env`:
```
DATABASE_URL=postgresql://username:password@localhost:5432/backend_db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

### 4. Create PostgreSQL Database

```bash
# Using psql
createdb backend_db
```

Or use your preferred PostgreSQL client.

### 5. Run the Application

```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints

### Documentation
- **Interactive API Docs**: http://127.0.0.1:8000/docs (Swagger UI)
- **Alternative API Docs**: http://127.0.0.1:8000/redoc (ReDoc)

### Authentication
- **POST** `/api/v1/auth/register` - Register a new user
- **POST** `/api/v1/auth/login` - Login and get JWT token
- **GET** `/api/v1/auth/me` - Get current user info (requires token)

### Users
- **GET** `/api/v1/users` - List all users (requires token)
- **GET** `/api/v1/users/{user_id}` - Get specific user (requires token)
- **PUT** `/api/v1/users/{user_id}` - Update user info (requires token)
- **DELETE** `/api/v1/users/{user_id}` - Delete user (requires token)

### Health
- **GET** `/health` - Health check
- **GET** `/` - Root endpoint

## Example Usage

### Register a User

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "john_doe",
    "full_name": "John Doe",
    "password": "securepassword123"
  }'
```

### Login

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "john_doe",
    "full_name": "John Doe",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2024-03-10T10:00:00",
    "updated_at": null
  }
}
```

### Get Current User (with token)

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Database Migrations (Optional)

To use Alembic for database migrations:

```bash
# Initialize Alembic
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## Security Notes

⚠️ **Important for Production:**

1. Change `SECRET_KEY` to a strong, random value
2. Set `DEBUG=False` in production
3. Update `CORS` allowed origins
4. Use environment variables from a secure vault
5. Enable HTTPS/SSL
6. Use strong database passwords
7. Implement rate limiting
8. Add input validation and sanitization
9. Use database connection pooling
10. Implement logging and monitoring

## Technologies Used

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **Bcrypt** - Password hashing
- **Uvicorn** - ASGI server

## License

MIT
