# Classify HNG 

A Django REST API that classifies people based on their names by predicting their **gender**, **age**, and **nationality**. Built with modern Python and deployed on Vercel.

## Purpose

Classify HNG allows you to submit a name and receive comprehensive demographic predictions including:
- **Gender** with probability score
- **Age** estimate with age group classification
- **Country/Nationality** with probability score
- Historical data tracking

Perfect for data enrichment, user profiling, or demographic analysis workflows.

---

## Quick Start

### Prerequisites
- Python 3.13+
- PostgreSQL database (Supabase recommended)
- pip & virtualenv

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd classify_hng
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```
   DATABASE_URL=postgres://username:password@host:port/database?sslmode=require
   ```

5. **Run migrations**
   ```bash
   python3 manage.py migrate
   ```

6. **Start development server**
   ```bash
   python3 manage.py runserver
   ```

The API will be available at `http://localhost:8000`

---

## API Endpoints

### 1. Create User Profile
**Classify a person by name**

- **Endpoint:** `POST /api/profiles`
- **Request Body:**
  ```json
  {
    "name": "John"
  }
  ```

- **Success Response (200):**
  ```json
  {
    "status": "success",
    "message": "Profile already exists",
    "data": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "john",
      "gender": "male",
      "gender_probability": 0.99,
      "sample_size": 1250,
      "age": 42,
      "age_group": "35-50",
      "country_id": "US",
      "country_probability": 0.85,
      "created_at": "2026-04-20T10:30:00Z"
    }
  }
  ```

- **Error Response (400):**
  ```json
  {
    "status": "error",
    "message": "Name is required"
  }
  ```

- **Error Response (422):**
  ```json
  {
    "status": "error",
    "message": "Name cannot be a number"
  }
  ```

### 2. Get User Profile
**Retrieve a previously classified user**

- **Endpoint:** `GET /api/profiles/<user_id>`
- **Success Response (200):**
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "john",
    "gender": "male",
    "age": 42,
    "age_group": "35-50",
    "country_id": "US"
  }
  ```

---

## Project Structure

```
classify_hng/
├── classifi/                 # Django project settings
│   ├── settings.py          # Configuration (DB, CORS, etc)
│   ├── urls.py              # Project-level URL routing
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── classify/                # Main API application
│   ├── models.py            # User data model
│   ├── views.py             # API view logic
│   ├── serializers.py       # Data serialization
│   ├── urls.py              # App-level URL routing
│   ├── admin.py             # Django admin configuration
│   └── migrations/          # Database migrations
├── manage.py                # Django management script
├── .env                     # Environment variables (not in git)
├── requirements.txt         # Python dependencies
└── db.sqlite3               # SQLite database (development only)
```

---

## Data Sources

The API integrates with three external APIs to gather demographic information:

| Data | API | Endpoint |
|------|-----|----------|
| **Gender** | [Genderize.io](https://genderize.io) | `https://api.genderize.io` |
| **Age** | [Agify.io](https://agify.io) | `https://api.agify.io` |
| **Nationality** | [Nationalize.io](https://nationalize.io) | `https://api.nationalize.io` |

---

## Database Model

### User
```python
id                    # UUID v7 (auto-generated)
name                  # Person's name (string)
gender                # Predicted gender (male/female)
gender_probability    # Confidence score (0-1)
sample_size           # API sample size for the prediction
age                   # Predicted age (integer)
age_group             # Age bracket (e.g., "35-50")
country_id            # ISO country code (e.g., "US")
country_probability   # Confidence score (0-1)
created_at            # Timestamp of record creation
```

---

## Configuration

### Key Settings (classifi/settings.py)

| Setting | Value | Purpose |
|---------|-------|---------|
| `DEBUG` | `True` (dev) / `False` (prod) | Enable debug mode |
| `ALLOWED_HOSTS` | `["*"]` | Allowed request hosts |
| `CORS_ALLOW_ALL_ORIGINS` | `True` | Enable cross-origin requests |
| `DATABASE_ENGINE` | PostgreSQL | Production database |

### Environment Variables

```
DATABASE_URL     # PostgreSQL connection string with SSL
```

---

## Development

### Run Tests
```bash
python3 manage.py test
```

### Check Project Status
```bash
python3 manage.py check
```

### Create Superuser
```bash
python3 manage.py createsuperuser
```

### Access Django Admin
Navigate to `http://localhost:8000/admin`

---

## Dependencies

Key packages (see `requirements.txt` for full list):
- **Django** - Web framework
- **djangorestframework** - REST API toolkit
- **django-cors-headers** - CORS support
- **psycopg2-binary** - PostgreSQL adapter
- **dj-database-url** - Database URL parsing
- **python-dotenv** - Environment variable management
- **httpx** - HTTP client for external APIs

---

## Deployment

### Deploy to Vercel

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Deploy to production**
   ```bash
   vercel --prod
   ```

3. **Set environment variables** on Vercel dashboard:
   - `DATABASE_URL` - PostgreSQL connection string

---

## Common Issues

### Database Connection Error
```
Error loading psycopg2 or psycopg module
```
**Solution:** Install the database driver
```bash
pip install psycopg2-binary
```

### Invalid DSN Error
```
invalid dsn: invalid connection option "supa"
```
**Solution:** Check `.env` file has a valid PostgreSQL URL format

### CORS Error in Frontend
If requests are blocked, verify `CORS_ALLOW_ALL_ORIGINS = True` in `settings.py`

---

## Example Usage

### Using cURL
```bash
# Create profile
curl -X POST http://localhost:8000/api/profiles \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'

# Get profile
curl http://localhost:8000/api/profiles/550e8400-e29b-41d4-a716-446655440000
```

### Using Python
```python
import httpx

# Create profile
response = httpx.post(
    "http://localhost:8000/api/profiles",
    json={"name": "Bob"}
)
user_data = response.json()

# Get profile
profile = httpx.get(
    f"http://localhost:8000/api/profiles/{user_data['data']['id']}"
)
print(profile.json())
```

---

## License

This project is part of the HNG internship program.

---

## Tips

- **Cache results:** Store user profiles to avoid repeated API calls
- **Error handling:** Always check the `status` field in responses
- **Rate limiting:** External APIs may have rate limits; implement retry logic
- **Validation:** The API validates that names are not purely numeric

---

## Support

For issues or questions:
1. Check the error messages in API responses
2. Review `classifi/settings.py` for configuration
3. Verify external API services are accessible

---

**Built with ❤️ using Django & REST framework**
