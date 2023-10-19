from django.urls import path
from . import views

urlpatterns = [
    path('record_expense/', views.ExpenseCreateView.as_view(), name='record_expense'),
    path('balances/', views.BalanceListView.as_view(), name='balance-list'),
]