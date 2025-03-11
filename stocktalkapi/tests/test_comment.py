from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from stocktalkapi.models import User, Post, Comment

class CommentAPITestCase(APITestCase):

    def setUp(self):
        """Set up a test user, post, and comment for use in test cases"""
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

        self.comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content="This is a test comment."
        )

    def test_list_comments(self):
        """Test retrieving a list of comments"""
        url = reverse('comment-list')  # Ensure your ViewSet uses 'basename=comment' in routers
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], "This is a test comment.")

    def test_get_single_comment(self):
        """Test retrieving a single comment"""
        url = reverse('comment-detail', args=[self.comment.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], "This is a test comment.")

    def test_create_comment(self):
        """Test creating a new comment"""
        url = reverse('comment-list')
        data = {
            "post": self.post.id,
            "user": self.user.id,
            "content": "This is a new comment."
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.last().content, "This is a new comment.")

    def test_update_comment(self):
        """Test updating an existing comment"""
        url = reverse('comment-detail', args=[self.comment.id])
        data = {
            "post": self.post.id,
            "user": self.user.id,
            "content": "This is an updated comment."
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, "This is an updated comment.")

    def test_delete_comment(self):
        """Test deleting a comment"""
        url = reverse('comment-detail', args=[self.comment.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
