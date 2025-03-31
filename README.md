# Project Manager Interview Exercise

This Django project serves as a foundation for technical interviews, providing candidates with a pre-configured environment to demonstrate their skills in backend development.

## Project Overview

The project implements a basic project management system with the following features:
- Project tracking with status and dates
- Task management with assignments
- RESTful API endpoints
- Pre-populated test data

## Technical Stack

- Python/Django
- Django REST Framework
- SQLite database
- Debug Toolbar for development

## Project Structure

```
.
├── config/             # Project configuration
├── core/              # Core functionality
├── project_manager/   # Main app for project/task management
└── manage.py         # Django management script
```

## Getting Started

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Available Endpoints

- `GET /api/projects/list/` - List all projects
- `GET /api/tasks/list/` - List all tasks

## Test Data

The project includes migrations that automatically create test data:
- 5 sample users with different roles
- 5 projects with varying statuses and dates
- Multiple tasks per project with random assignments

## For Interviewers

This project is designed to be used as a starting point for technical interviews. Some suggested exercises:
- Add new API endpoints
- Implement filtering and sorting
- Add authentication and permissions
- Extend the data model
- Add unit tests
- Implement task dependencies
- Add project/task statistics

## For Candidates

When working with this project:
1. Take time to understand the existing code structure
2. Follow the established patterns and conventions
3. Consider edge cases in your implementations
4. Document any significant changes or additions
5. Write clean, maintainable code

## License

This project is provided for interview purposes only. All rights reserved.
