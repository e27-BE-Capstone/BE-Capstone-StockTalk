from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from stocktalkapi.models import Comment, User, Post

class CommentView(ViewSet):
    def retrieve(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except Comment.DoesNotExist as ex:
            return Response({'message': str(ex)}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            user = User.objects.get(pk=request.data["user"])
            post = Post.objects.get(pk=request.data["post"])
            comment = Comment.objects.create(
                user=user,
                post=post,
                content=request.data["content"]
            )
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"message": f"Missing required field: {e.args[0]}"}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, Post.DoesNotExist):
            return Response({"message": "User or Post not found"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            if "content" in request.data:
                comment.content = request.data["content"]
            comment.save()
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'content', 'created_at', 'updated_at')
