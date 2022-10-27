"""Account URLs."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import transactions as transaction_views
from .views import monthly_bills as monthlybills_views

router = DefaultRouter()
router.register(
    r"transactions", transaction_views.TransactionViewSet, basename="transactions"
   # r"monthly_bills", monthlybills_views.MonthlyBillsViewSet, basedname="monthlybills"
)

urlpatterns = [path("", include(router.urls))]
