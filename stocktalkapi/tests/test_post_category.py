from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from stocktalkapi.models import Category, Post, PostCategory, User

class PostCategoryAPITestCase(APITestCase):

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create(name="John Doe", email="john@example.com")
        self.post = Post.objects.create(
            user=self.user,
            title="Stock Market Trends",
            content="Discussion on latest stock market movements.",
            media="https://example.com/image.jpg"
        )
        self.category = Category.objects.create(
            name="Finance",
            description="Discussion on financial topics."
        )
        self.post_category = PostCategory.objects.create(post=self.post, category=self.category)

    def test_list_post_categories(self):
        """Test retrieving a list of PostCategory relationships"""
        url = reverse('postcategory-list')  
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_single_post_category(self):
        """Test retrieving a single PostCategory relationship"""
        url = reverse('postcategory-detail', args=[self.post_category.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['post']['id'], self.post.id)
        self.assertEqual(response.data['category']['id'], self.category.id)

    def test_create_post_category(self):
        """Test creating a new PostCategory relationship"""
        new_category = Category.objects.create(name="Technology", description="Tech-related posts")
        url = reverse('postcategory-list')
        data = {
            "post": self.post.id,
            "category": new_category.id
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PostCategory.objects.count(), 2)

    def test_create_post_category_missing_field(self):
        """Test failing to create PostCategory due to missing field"""
        url = reverse('postcategory-list')
        data = {"post": self.post.id}  # Missing category
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Missing required field", response.data['message'])

    def test_update_post_category(self):
        """Test updating an existing PostCategory"""
        new_category = Category.objects.create(name="Tech", description="Tech-related posts")
        url = reverse('postcategory-detail', args=[self.post_category.id])
        data = {"category": new_category.id}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post_category.refresh_from_db()
        self.assertEqual(self.post_category.category.id, new_category.id)

    def test_update_post_category_not_found(self):
        """Test updating a PostCategory that doesn't exist"""
        url = reverse('postcategory-detail', args=[999])  # Invalid ID
        data = {"category": self.category.id}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "PostCategory not found")

    def test_delete_post_category(self):
        """Test deleting a PostCategory relationship"""
        url = reverse('postcategory-detail', args=[self.post_category.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PostCategory.objects.filter(id=self.post_category.id).exists())

    def test_delete_post_category_not_found(self):
        """Test deleting a PostCategory that doesn't exist"""
        url = reverse('postcategory-detail', args=[999])  # Invalid ID
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "PostCategory not found")
