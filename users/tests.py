from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import CustomUser

class UserRegistrationTest(APITestCase):
    def test_register_user(self):
        url = reverse('users-list')  
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpass123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(CustomUser.objects.filter(email="testuser@example.com").exists())

    def test_register_user_with_existing_email(self):
        url = reverse('users-list')
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpass123"
        }
        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(CustomUser.objects.filter(email="testuser@example.com").exists())
    
    