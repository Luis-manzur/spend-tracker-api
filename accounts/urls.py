"""Account URLs."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import accounts as account_views

router = DefaultRouter()
router.register(r"accounts", account_views.AccountViewSet, basename="accounts")

urlpatterns = [path("", include(router.urls))]
