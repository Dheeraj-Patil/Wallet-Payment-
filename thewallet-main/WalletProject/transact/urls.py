from django.urls import path
from .views import (
    HomePageView, DashboardView, SendView, RequestView,
    HistoryView, AccountsView, PaymentIDView
)


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/send', SendView.as_view(), name='send'),
    path('dashboard/request', RequestView.as_view(), name='request'),
    path('dashboard/history', HistoryView.as_view(), name='history'),
    path('dashboard/accounts', AccountsView.as_view(), name='accounts'),
    path('dashboard/pid', PaymentIDView.as_view(), name='pid'),
]
