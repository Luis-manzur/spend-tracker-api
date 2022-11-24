"""Users views."""

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.models.friends import FriendRequest
from users.permissions import IsAccountOwner
from users.serializers import (
    AccountVerificationSerializer,
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    FriendsSerializer,
)
from users.serializers.friends import (
    FriendRequestModelSerializer,
    CreateFriendRequestModelSerializer,
    AcceptFriendRequestSerializer,
)
from users.serializers.profiles import ProfileModelSerializer


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """User view set.
    Handle sign up, login and account verification.
    """

    queryset = User.objects.filter(is_active=True)
    lookup_field = "username"

    def get_serializer_class(self):
        """Assign serializer based on action"""
        if self.action == "signup":
            return UserSignUpSerializer
        elif self.action == "login":
            return UserLoginSerializer
        elif self.action == "verify":
            return AccountVerificationSerializer
        elif self.action == "profile":
            return ProfileModelSerializer
        elif self.action == "send_friend_request":
            return CreateFriendRequestModelSerializer
        elif self.action == "accept_friend_request":
            return AcceptFriendRequestSerializer
        else:
            return UserModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ["signup", "login", "verify"]:
            permissions = [AllowAny]
        elif self.action in ["retrieve", "update", "partial_update", "profile"]:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False, methods=["post"])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {"user": UserModelSerializer(user).data, "access_token": token}
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"message": "Congratulations, lets save some money!"}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["put", "patch"])
    def profile(self, request, *args, **kwargs):
        """Update profile data."""
        user = self.get_object()
        profile = user.profile
        partial = request.method == "PATCH"
        serializer = ProfileModelSerializer(profile, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)

    @action(detail=False, url_path="send-friend-requests", methods=["post"])
    def send_friend_request(self, request, *args, **kwargs):
        try:
            to_user = User.objects.get(username=request.data["to_user"])
            if not to_user:
                raise Exception("This username doesn't exist")
            from_user = request.user
            friend_request, created = FriendRequest.objects.get_or_create(
                from_user=from_user, to_user=to_user
            )
            if created:
                message = {"message": "Friend request sent successfully!"}
            else:
                message = {"message": "Friend request already sent!"}
        except Exception as e:
            message = {f"message": f"Friend request failed because {e}"}

        return Response(message, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="accept-friend-requests")
    def accept_friend_request(self, request, *args, **kwargs):
        try:
            friend_request = FriendRequest.objects.get(id=request.data["id"])
            if friend_request.to_user == request.user:
                friend_request.to_user.friends.add(friend_request.from_user)
                friend_request.from_user.friends.add(friend_request.to_user)
                message = {"message": "Friend request accepted successfully!"}
            else:
                message = {"message": "Friend request not yours!"}
        except Exception as e:
            message = {f"message": f"Friend request failed because '{e}'"}

        return Response(message, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="get-friend-requests")
    def get_friend_requests(self, request, *args, **kwargs):
        friend_requests = FriendRequest.objects.filter(to_user=request.user)
        data = FriendRequestModelSerializer(friend_requests, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="get-friends")
    def get_friend_request(self, request, *args, **kwargs):
        data = FriendsSerializer(request.user).data
        return Response(data, status=status.HTTP_200_OK)
