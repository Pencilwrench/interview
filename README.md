# Interview Exercise

This Django project serves as a foundation for technical interviews, providing candidates with a pre-configured environment to demonstrate their skills in backend development.

## Project Overview

The project implements a basic project management system with the following features:

- Project tracking with status and dates
- Task management with assignments
- RESTful API endpoints
- Pre-populated test data

## Questions / Challenges

- How would you optimize the tasks list endpoint?
- How would you customize the task admin page?
- Ensure due date on the task model does not allow past dates
- Protect a project from being deleted if it has tasks
- Introduce a Team model. A user can belong to multiple teams. Project tasks must be assigned to a team member.

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
5. Create super user
   ```bash
   python manage.py createsuperuser
   ```
6. Start the development server:
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

## For Candidates

When working with this project:

1. Take time to understand the existing code structure
2. Follow the established patterns and conventions
3. Document any significant changes or additions
4. Write clean, maintainable code

## License

This project is provided for interview purposes only. All rights reserved.
