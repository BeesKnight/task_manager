from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password='testpass123')
        self.other = User.objects.create_user('bob', password='testpass123')
        self.task = Task.objects.create(owner=self.user, title='Own task')
        self.other_task = Task.objects.create(owner=self.other, title='Other task')

    def test_authorization_required(self):
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response['Location'])

    def test_list_filters_by_owner(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('tasks:task_list'))
        self.assertContains(response, 'Own task')
        self.assertNotContains(response, 'Other task')

    def test_owner_is_assigned_on_create(self):
        self.client.login(username='alice', password='testpass123')
        self.client.post(
            reverse('tasks:new_task'),
            {'title': 'Created', 'description': '', 'priority': Task.HIGH},
        )
        task = Task.objects.get(title='Created')
        self.assertEqual(task.owner, self.user)

    def test_cannot_edit_other_task(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(
            reverse('tasks:edit_task', args=[self.other_task.id]),
            {'title': 'Hacked', 'description': '', 'priority': Task.LOW},
        )
        self.assertEqual(response.status_code, 404)
        self.other_task.refresh_from_db()
        self.assertEqual(self.other_task.title, 'Other task')

    def test_cannot_delete_other_task(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(reverse('tasks:delete_task', args=[self.other_task.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(id=self.other_task.id).exists())

    def test_missing_id_returns_404(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('tasks:edit_task', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_toggle_task(self):
        self.client.login(username='alice', password='testpass123')
        self.client.post(reverse('tasks:toggle_task', args=[self.task.id]))
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)

    def test_delete_requires_post(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('tasks:delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
