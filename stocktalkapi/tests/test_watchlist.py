from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from stocktalkapi.models import User, Watchlist
from decimal import Decimal

class WatchlistAPITestCase(APITestCase):

    def setUp(self):
        """Set up a test user and watchlist entry for use in test cases"""
        self.user = User.objects.create(
            name="Test User",
            email="testuser@example.com",
            image="https://example.com/test-image.jpg",
            bio="This is a test user",
            reputation=10
        )

        self.watchlist = Watchlist.objects.create(
            user=self.user,
            stock_name="AAPL",
            stock_price=Decimal('150.75'),
            stock_notes="Apple stock looks promising"
        )

    def test_list_watchlist(self):
        """Test retrieving a list of watchlist entries"""
        url = reverse('watchlist-list')  # Ensure your ViewSet uses 'basename=watchlist' in routers
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['stock_name'], "AAPL")

    def test_get_single_watchlist(self):
        """Test retrieving a single watchlist entry"""
        url = reverse('watchlist-detail', args=[self.watchlist.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stock_price'], "150.75")

    def test_create_watchlist_entry(self):
        """Test creating a new watchlist entry"""
        url = reverse('watchlist-list')
        data = {
            "user": self.user.id,
            "stock_name": "GOOGL",
            "stock_price": "2800.50",
            "stock_notes": "Google stock is stable"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Watchlist.objects.count(), 2)
        self.assertEqual(Watchlist.objects.last().stock_name, "GOOGL")

    def test_update_watchlist_entry(self):
        """Test updating an existing watchlist entry"""
        url = reverse('watchlist-detail', args=[self.watchlist.id])
        data = {
            "user": self.user.id,
            "stock_name": "AAPL",
            "stock_price": "160.00",
            "stock_notes": "Updated price prediction"
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.watchlist.refresh_from_db()
        self.assertEqual(self.watchlist.stock_price, Decimal('160.00'))
        self.assertEqual(self.watchlist.stock_notes, "Updated price prediction")

    def test_delete_watchlist_entry(self):
        """Test deleting a watchlist entry"""
        url = reverse('watchlist-detail', args=[self.watchlist.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Watchlist.objects.count(), 0)
