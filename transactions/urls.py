"""Account URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import transactions as transaction_views

router = DefaultRouter()
router.register(
    r"transactions", transaction_views.TransactionViewSet, basename="transactions"
)

urlpatterns = [path("", include(router.urls))]
