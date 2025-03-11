from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from stocktalkapi.models import User, Post

class PostAPITestCase(APITestCase):

    def setUp(self):
        """Set up a test user and post for use in test cases"""
        self.user = User.objects.create(
            name="Test User",
            email="testuser@example.com",
            image="https://example.com/test-image.jpg",
            bio="This is a test user",
            reputation=10
        )

        self.post = Post.objects.create(
            user=self.user,
            title="Test Post",
            content="This is a test post content.",
            media="https://example.com/test-media.jpg"
        )

    def test_list_posts(self):
        """Test retrieving a list of posts"""
        url = reverse('post-list')  # Ensure your ViewSet uses 'basename=post' in routers
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Post")

    def test_get_single_post(self):
        """Test retrieving a single post"""
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Post")
        self.assertEqual(response.data['content'], "This is a test post content.")

    def test_create_post(self):
        """Test creating a new post"""
        url = reverse('post-list')
        data = {
            "user": self.user.id,
            "title": "New Post",
            "content": "This is a new test post.",
            "media": "https://example.com/new-media.jpg"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.last().title, "New Post")

    def test_update_post(self):
        """Test updating an existing post"""
        url = reverse('post-detail', args=[self.post.id])
        data = {
            "user": self.user.id,
            "title": "Updated Post",
            "content": "This is an updated post content.",
            "media": "https://example.com/updated-media.jpg"
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Post")
        self.assertEqual(self.post.content, "This is an updated post content.")

    def test_delete_post(self):
        """Test deleting a post"""
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
