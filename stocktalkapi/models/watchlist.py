from django.db import models
from stocktalkapi.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists')
    stock_name = models.CharField(max_length=100)
    stock_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.01, validators=[MinValueValidator(Decimal('0.01'))])
    stock_notes = models.TextField(blank=True, null=True)