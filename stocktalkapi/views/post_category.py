from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from stocktalkapi.models import PostCategory, Category, Post

class PostCategoryView(ViewSet):
    def retrieve(self, request, pk):
        """Handle GET request for a single PostCategory"""
        try:
            post_category = PostCategory.objects.get(pk=pk)
            serializer = PostCategorySerializer(post_category)
            return Response(serializer.data)
        except PostCategory.DoesNotExist:
            return Response({"message": "PostCategory not found"}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET request for all PostCategories"""
        post_categories = PostCategory.objects.all()
        serializer = PostCategorySerializer(post_categories, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST request to create a new PostCategory"""
        try:
            post = Post.objects.get(pk=request.data["post"])
            category = Category.objects.get(pk=request.data["category"])
            post_category = PostCategory.objects.create(post=post, category=category)
            serializer = PostCategorySerializer(post_category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"message": f"Missing required field: {e.args[0]}"}, status=status.HTTP_400_BAD_REQUEST)
        except (Post.DoesNotExist, Category.DoesNotExist):
            return Response({"message": "Post or Category not found"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT request to update a PostCategory"""
        try:
            post_category = PostCategory.objects.get(pk=pk)
            if "post" in request.data:
                post_category.post = Post.objects.get(pk=request.data["post"])
            if "category" in request.data:
                post_category.category = Category.objects.get(pk=request.data["category"])
            post_category.save()

            serializer = PostCategorySerializer(post_category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PostCategory.DoesNotExist:
            return Response({"message": "PostCategory not found"}, status=status.HTTP_404_NOT_FOUND)
        except (Post.DoesNotExist, Category.DoesNotExist):
            return Response({"message": "Post or Category not found"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Handle DELETE request to remove a PostCategory"""
        try:
            post_category = PostCategory.objects.get(pk=pk)
            post_category.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except PostCategory.DoesNotExist:
            return Response({"message": "PostCategory not found"}, status=status.HTTP_404_NOT_FOUND)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'content', 'media', 'created_at', 'updated_at')
        
class PostCategorySerializer(serializers.ModelSerializer):
    
    post = PostSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = PostCategory
        fields = ('id', 'post', 'category')


