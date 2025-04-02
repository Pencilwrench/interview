# Interview Exercise

This Django project serves as a foundation for technical interviews, providing candidates with a pre-configured environment to demonstrate their skills in backend development.

## Project Overview

The project implements a basic project management system with the following features:

- Project tracking with status and dates
- Task management with assignments
- RESTful API endpoints
- Pre-populated test data

## Questions

- The task list api needs optimization. How would you implement it?
- How would you ensure due date on the task model does not allow past dates?
- How would you protect a project from being deleted if it has tasks?
- Look at the Team model in models.py. How would you prevent a user from being assigned to a task that is not in their team?
- Look at TeamAdmin in admin.py. How would you help your staff to avoid assigning non team members to tasks, without relying on your previous question's solution?

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
