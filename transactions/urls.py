"""Account URLs."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import transactions as transaction_views

router = DefaultRouter()
router.register(
    r"transactions", transaction_views.TransactionViewSet, basename="transactions"
)

urlpatterns = [path("", include(router.urls))]
