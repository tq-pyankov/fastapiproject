# Task Management System with FastAPI

A modern task management system built with FastAPI that includes advanced features like task prioritization, team collaboration, and intelligent task assignment.

## Features

- User authentication and authorization
- CRUD operations for tasks, projects, and teams
- Intelligent task assignment algorithm
- Team collaboration features
- Task prioritization and tracking
- RESTful API with OpenAPI documentation

## Project Structure

```
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   └── api.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   ├── tests/
│   ├── alembic/
│   ├── requirements.txt
│   └── docker-compose.yml
```

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd task-management-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
DATABASE_URL=sqlite:///./task_management.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Initialize the database:
The application will automatically create the database and tables on first run. If you want to use Alembic for database migrations:

```bash
# Install Alembic if not already installed
pip install alembic

# Initialize Alembic
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply the migration
alembic upgrade head
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

## Testing

Run tests with:
```bash
pytest
```

## API Documentation

Once the application is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Business Logic

The system includes an intelligent task assignment algorithm that:
- Analyzes team member workload and expertise
- Considers task priorities and deadlines
- Optimizes task distribution for maximum efficiency
- Provides recommendations for task assignments

## License

MIT 