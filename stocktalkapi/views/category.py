from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from stocktalkapi.models import Category

class CategoryView(ViewSet):
    def retrieve(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            category = Category.objects.create(
                name=request.data["name"],
                description=request.data.get("description", "")
            )
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"message": f"Missing required field: {e.args[0]}"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            if "name" in request.data:
                category.name = request.data["name"]
            if "description" in request.data:
                category.description = request.data["description"]
            category.save()
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')
        