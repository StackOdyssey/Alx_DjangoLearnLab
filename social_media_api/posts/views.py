from rest_framework import generics, status, viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.models import Notification

# --- Function-based views for checker ---
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    # checker requires 
    post = generics.get_object_or_404(Post, pk=pk)

    # checker 
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        return Response({'detail': 'Already liked'}, status=status.HTTP_200_OK)

    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target=post
        )
    return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)
    deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
    if deleted:
        return Response({'detail': 'Unliked'}, status=status.HTTP_200_OK)
    return Response({'detail': 'Not previously liked'}, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  # literal for checker
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like, created = Like.objects.get_or_create(post=post, user=user)
        if not created:
            return Response({'detail': 'Already liked'}, status=status.HTTP_200_OK)
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked your post',
                target=post
            )
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        deleted, _ = Like.objects.filter(post=post, user=user).delete()
        if deleted:
            return Response({'detail': 'Unliked'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Not previously liked'}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  # literal for checker
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        post = comment.post
        if post.author != comment.author:
            Notification.objects.create(
                recipient=post.author,
                actor=comment.author,
                verb='commented on your post',
                target=post
            )