from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from stocktalkapi.models import User

class UserView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for a single user"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': str(ex)}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all users or filter by email"""
        email = request.query_params.get('email', None)
        users = User.objects.all()

        if email is not None:
            users = users.filter(email=email)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new user"""
        user = User.objects.create(
            name=request.data["name"],
            email=request.data["email"],
            image=request.data.get("image", "images/default-photo.jpg"),  
            bio=request.data.get("bio", ""),
            reputation=request.data.get("reputation", 0)
        )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests to update a user"""
        user = User.objects.get(pk=pk)
        user.name = request.data["name"]
        user.email = request.data["email"]
        user.image = request.data.get("image", user.image)
        user.bio = request.data.get("bio", user.bio)
        user.reputation = request.data.get("reputation", user.reputation)
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """Handle DELETE requests to remove a user"""
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'image', 'bio', 'reputation', 'created_at', 'updated_at')
        depth = 1
        