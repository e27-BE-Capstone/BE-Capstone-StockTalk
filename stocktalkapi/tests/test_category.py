from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from stocktalkapi.models import Category

class CategoryAPITestCase(APITestCase):

    def setUp(self):
        """Set up a test category for use in test cases"""
        self.category = Category.objects.create(
            name="Technology",
            description="Discussion about the latest in tech."
        )

    def test_list_categories(self):
        """Test retrieving a list of categories"""
        url = reverse('category-list')  # Ensure your ViewSet uses 'basename=category' in routers
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Technology")

    def test_get_single_category(self):
        """Test retrieving a single category"""
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Technology")
        self.assertEqual(response.data['description'], "Discussion about the latest in tech.")

    def test_create_category(self):
        """Test creating a new category"""
        url = reverse('category-list')
        data = {
            "name": "Finance",
            "description": "Stock market and financial discussions."
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.last().name, "Finance")

    def test_update_category(self):
        """Test updating an existing category"""
        url = reverse('category-detail', args=[self.category.id])
        data = {
            "name": "Updated Technology",
            "description": "Updated description for tech discussions."
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Technology")
        self.assertEqual(self.category.description, "Updated description for tech discussions.")

    def test_delete_category(self):
        """Test deleting a category"""
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
