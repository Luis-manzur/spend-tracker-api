from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from transactions.models import Goal
from transactions.permissions import IsTransactionsOwner
from transactions.serializers import (
    GoalModelSerializer,
    CreateGoalModelSerializer,
)


class GoalsViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ("name", "description")
    ordering_fields = ("amount", "created", "-created")
    ordering = (
        "-created",
        "amount",
    )
    filter_fields = ("name",)

    def get_queryset(self):
        queryset = Goal.objects.all()
        if self.action == "list":
            queryset = Goal.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self):
        """Assign serializer based on action"""
        if self.action in ["create"]:
            return CreateGoalModelSerializer
        else:
            return GoalModelSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsTransactionsOwner, IsAuthenticated]

        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        goal = serializer.save()
        goal = GoalModelSerializer(goal).data
        headers = self.get_success_headers(goal)
        return Response(goal, status=status.HTTP_201_CREATED, headers=headers)
