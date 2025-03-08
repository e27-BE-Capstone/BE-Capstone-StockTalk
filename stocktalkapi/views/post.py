from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from stocktalkapi.models import Post, User

class PostView(ViewSet):
    def retrieve(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': str(ex)}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            user = User.objects.get(pk=request.data["user"])
            post = Post.objects.create(
                user=user,
                title=request.data["title"],
                content=request.data["content"],
                media=request.data.get("media", "")
            )
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"message": f"Missing required field: {e.args[0]}"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            if "user" in request.data:
                post.user = User.objects.get(pk=request.data["user"])
            if "title" in request.data:
                post.title = request.data["title"]
            if "content" in request.data:
                post.content = request.data["content"]
            if "media" in request.data:
                post.media = request.data["media"]
            post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'content', 'media', 'created_at', 'updated_at')