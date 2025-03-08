from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from stocktalkapi.models import Watchlist, User

class WatchlistView(ViewSet):
    def retrieve(self, request, pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk)
            serializer = WatchlistSerializer(watchlist)
            return Response(serializer.data)
        except Watchlist.DoesNotExist:
            return Response({"message": "Watchlist not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        watchlists = Watchlist.objects.all()
        serializer = WatchlistSerializer(watchlists, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        try:
            user = User.objects.get(pk=request.data["user"])
            watchlist = Watchlist.objects.create(
                user=user,
                stock_name=request.data["stock_name"],
                stock_price=request.data["stock_price"],
                stock_notes=request.data.get("stock_notes", "")
            )
            serializer = WatchlistSerializer(watchlist)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"message": f"Missing required field: {e.args[0]}"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk)
            if "stock_name" in request.data:
                watchlist.stock_name = request.data["stock_name"]
            if "stock_price" in request.data:
                watchlist.stock_price = request.data["stock_price"]
            if "stock_notes" in request.data:
                watchlist.stock_notes = request.data["stock_notes"]
            watchlist.save()
            serializer = WatchlistSerializer(watchlist)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Watchlist.DoesNotExist:
            return Response({"message": "Watchlist not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk)
            watchlist.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Watchlist.DoesNotExist:
            return Response({"message": "Watchlist not found"}, status=status.HTTP_404_NOT_FOUND)

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ('id', 'user', 'stock_name', 'stock_price', 'stock_notes')
        