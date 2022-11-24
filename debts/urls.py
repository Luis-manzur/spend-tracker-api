"""Debt URLs."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import debts as debt_views

router = DefaultRouter()
router.register(r"debts", debt_views.DebtViewSet, basename="debts")

urlpatterns = [path("", include(router.urls))]
