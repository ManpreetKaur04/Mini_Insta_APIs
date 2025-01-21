from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Post, Follower, UserAction
from .serializers import UserSerializer, PostSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def followers(self, request, username=None):
        """
        List all followers of a specific user.
        """
        try:
            user = User.objects.get(username=username)
            followers = Follower.objects.filter(following=user).select_related('follower')
            data = [{'username': follower.follower.username, 'name': follower.follower.get_full_name()} for follower in followers]
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def following(self, request, username=None):
        """
        List all users a specific user is following.
        """
        try:
            user = User.objects.get(username=username)
            following = Follower.objects.filter(follower=user).select_related('following')
            data = [{'username': following_user.following.username, 'name': following_user.following.get_full_name()} for following_user in following]
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def actions(self, request):
        """
        Retrieve a list of users hidden/blocked by the logged-in user.
        """
        user_actions = UserAction.objects.filter(user=request.user).select_related('target_user')
        data = [{'username': action.target_user.username, 'action': action.action} for action in user_actions]
        return Response(data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'])
    def follow(self, request, username=None):
        try:
            user_to_follow = User.objects.get(username=username)
            if user_to_follow == request.user:
                return Response({'error': 'Cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
            if UserAction.objects.filter(user=request.user, target_user=user_to_follow, action='BLOCK').exists():
                return Response({'error': 'You have blocked this user and cannot follow them.'}, status=status.HTTP_400_BAD_REQUEST)
            Follower.objects.create(follower=request.user, following=user_to_follow)
            return Response({'status': 'followed'})
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
       

    @action(detail=True, methods=['post'])
    def unfollow(self, request, username=None):
        try:
            user_to_unfollow = User.objects.get(username=username)
            if not Follower.objects.filter(follower=request.user, following=user_to_unfollow).exists():
                return Response({'error': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)
            Follower.objects.filter(follower=request.user, following=user_to_unfollow).delete()
            return Response({'status': 'unfollowed'})
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        finally:
            pass

    @action(detail=True, methods=['post', 'delete'])
    def action(self, request, username=None):
        try:
            target_user = User.objects.get(username=username)
            if target_user == request.user:
                return Response({'error': 'Cannot block yourself.'}, status=status.HTTP_400_BAD_REQUEST)

            if request.method == 'POST':
                action = request.data.get('action')
                if action not in ['HIDE', 'BLOCK']:
                    return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
                if UserAction.objects.filter(user=request.user, target_user=target_user, action=action).exists():
                    return Response({'error': f'User already {action.lower()}ed.'}, status=status.HTTP_400_BAD_REQUEST)
                UserAction.objects.create(user=request.user, target_user=target_user, action=action)
                return Response({'status': f'{action.lower()}ed'})
            elif request.method == 'DELETE':
                UserAction.objects.filter(user=request.user, target_user=target_user).delete()
                return Response({'status': 'action removed'})
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)