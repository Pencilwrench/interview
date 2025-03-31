import random
from datetime import date, timedelta
from django.db import migrations
from django.utils.timezone import now


def create_test_data(apps, schema_editor):
    # Get the models
    User = apps.get_model('auth', 'User')
    Project = apps.get_model('project_manager', 'Project')
    Task = apps.get_model('project_manager', 'Task')

    # Create 5 users with realistic names
    user_data = [
        ('jsmith', 'John Smith', 'Engineering Lead'),
        ('agarcia', 'Ana Garcia', 'Product Manager'),
        ('mchen', 'Michael Chen', 'Senior Developer'),
        ('spatel', 'Sarah Patel', 'UX Designer'),
        ('rwilson', 'Robert Wilson', 'QA Engineer')
    ]
    
    users = []
    for username, full_name, _ in user_data:
        first_name, last_name = full_name.split()
        user = User.objects.create_user(
            username=username,
            email=f'{username}@company.com',
            password='testpass123',
            first_name=first_name,
            last_name=last_name
        )
        users.append(user)

    # Create 5 projects with realistic names and descriptions
    project_data = [
        ('Mobile App Redesign', 'Redesign and modernize our mobile application UI/UX for better user engagement'),
        ('Cloud Migration Phase 1', 'Migrate core services to cloud infrastructure for improved scalability'),
        ('Customer Portal Enhancement', 'Implement new features and security improvements in the customer portal'),
        ('API Integration Platform', 'Develop a centralized platform for third-party API integrations'),
        ('Performance Optimization', 'Optimize database queries and application performance for better response times')
    ]
    
    project_statuses = ['active', 'completed']
    today = date.today()
    projects = []
    
    for name, description in project_data:
        start_date = today - timedelta(days=random.randint(1, 30))
        end_date = start_date + timedelta(days=random.randint(30, 90))
        
        project = Project.objects.create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            status=random.choice(project_statuses)
        )
        projects.append(project)

    # Common task templates that can be adapted for each project
    task_templates = [
        ('Requirements Documentation', 'Create detailed requirements documentation for {}'),
        ('Technical Design', 'Develop technical design specifications for {}'),
        ('Implementation', 'Implement core functionality for {}'),
        ('Code Review', 'Conduct code review for {} implementation'),
        ('Testing', 'Perform comprehensive testing for {}'),
        ('Documentation', 'Create user and technical documentation for {}'),
        ('Security Review', 'Conduct security assessment for {}'),
        ('Performance Testing', 'Execute performance tests for {}'),
        ('Deployment Planning', 'Prepare deployment strategy for {}'),
        ('Stakeholder Review', 'Present {} to stakeholders for feedback')
    ]

    task_statuses = ['pending', 'done']
    
    for project in projects:
        num_tasks = random.randint(5, 10)
        selected_tasks = random.sample(task_templates, num_tasks)
        
        for task_name, task_desc_template in selected_tasks:
            due_date = project.end_date - timedelta(days=random.randint(1, 30))
            Task.objects.create(
                project=project,
                title=task_name,
                description=task_desc_template.format(project.name),
                assigned_to=random.choice(users),
                due_date=due_date,
                status=random.choice(task_statuses)
            )


def remove_test_data(apps, schema_editor):
    # Get the models
    User = apps.get_model('auth', 'User')
    Project = apps.get_model('project_manager', 'Project')
    Task = apps.get_model('project_manager', 'Task')
    
    # Delete all users except superusers
    User.objects.filter(is_superuser=False).delete()
    
    # Delete all projects and tasks
    Project.objects.all().delete()
    Task.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('project_manager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_test_data, remove_test_data),
    ]
