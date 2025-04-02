from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from ..models import Project, Task, Team


class TaskAssignmentTests(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(
            username='user1',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password123'
        )
        
        # Create teams
        self.team1 = Team.objects.create(name='Team 1')
        self.team1.members.add(self.user1)
        
        self.team2 = Team.objects.create(name='Team 2')
        self.team2.members.add(self.user2)
        
        # Create projects
        self.project1 = Project.objects.create(
            name='Project 1',
            description='Test project 1',
            start_date='2025-01-01',
            end_date='2025-12-31',
            status='active',
            team=self.team1
        )
        
        self.project2 = Project.objects.create(
            name='Project 2',
            description='Test project 2',
            start_date='2025-01-01',
            end_date='2025-12-31',
            status='active',
            team=self.team2
        )
        
        # Create tasks
        self.task1 = Task.objects.create(
            project=self.project1,
            title='Task 1',
            description='Test task 1',
            assigned_to=self.user2,
            due_date='2025-06-01',
            status='pending'
        )
        
        self.task2 = Task.objects.create(
            project=self.project1,
            title='Task 2',
            description='Test task 2',
            assigned_to=self.user2,
            due_date='2025-06-01',
            status='pending'
        )
        
        # URL for bulk assignment
        self.url = reverse('bulk_task_assignment')
    
    def test_bulk_assign_success(self):
        """Test successful bulk assignment."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.url, {
            'task_ids': [self.task1.id, self.task2.id],
            'user_id': self.user1.id
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['metadata']['total_updated'], 2)
        self.assertEqual(response.data['metadata']['assignee'], 'user1')
        self.assertEqual(len(response.data['items']), 2)
    
    def test_bulk_assign_unauthorized(self):
        """Test unauthorized access."""
        response = self.client.post(self.url, {
            'task_ids': [self.task1.id],
            'user_id': self.user1.id
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_bulk_assign_wrong_team(self):
        """Test assigning tasks to user not in team."""
        self.client.force_authenticate(user=self.user1)
        task3 = Task.objects.create(
            project=self.project2,  # Project in team2
            title='Task 3',
            description='Test task 3',
            assigned_to=self.user2,
            due_date='2025-06-01',
            status='pending'
        )
        
        response = self.client.post(self.url, {
            'task_ids': [task3.id],
            'user_id': self.user1.id  # user1 is not in team2
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cannot be assigned to tasks in teams", response.data['error'])
    
    def test_bulk_assign_nonexistent_task(self):
        """Test assigning nonexistent task."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.url, {
            'task_ids': [99999],
            'user_id': self.user1.id
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("One or more tasks do not exist", response.data['error'])
    
    def test_bulk_assign_nonexistent_user(self):
        """Test assigning to nonexistent user."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.url, {
            'task_ids': [self.task1.id],
            'user_id': 99999
        })
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'User not found')
    
    def test_bulk_assign_empty_tasks(self):
        """Test assigning empty task list."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.url, {
            'task_ids': [],
            'user_id': self.user1.id
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("task_ids", response.data['error'])
