from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from stocktalkapi.models import User

class UserAPITestCase(APITestCase):

    def setUp(self):
        """Set up a test user for use in test cases"""
        self.user = User.objects.create(
            name="Test User",
            email="testuser@example.com",
            image="https://example.com/test-image.jpg",
            bio="This is a test user",
            reputation=10
        )

    def test_list_users(self):
        """Test retrieving a list of users"""
        url = reverse('user-list')  # Ensure your ViewSet uses 'basename=user' in routers
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test User")

    def test_get_single_user(self):
        """Test retrieving a single user"""
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], "testuser@example.com")

    def test_create_user(self):
        """Test creating a new user"""
        url = reverse('user-list')
        data = {
            "name": "New User",
            "email": "newuser@example.com",
            "image": "https://example.com/new-image.jpg",
            "bio": "This is a new user",
            "reputation": 5
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().name, "New User")

    def test_update_user(self):
        """Test updating an existing user"""
        url = reverse('user-detail', args=[self.user.id])
        data = {
            "name": "Updated User",
            "email": "updateduser@example.com",
            "image": "https://example.com/updated-image.jpg",
            "bio": "Updated bio",
            "reputation": 20
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Updated User")
        self.assertEqual(self.user.reputation, 20)

    def test_delete_user(self):
        """Test deleting a user"""
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
