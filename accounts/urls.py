"""Account URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import accounts as account_views

router = DefaultRouter()
router.register(r"accounts", account_views.AccountViewSet, basename="accounts")

urlpatterns = [path("", include(router.urls))]
