from django.urls import path

from transactions import views

app_name = 'transactions'


urlpatterns = [
    path('deposit/', views.DepositCreateView.as_view(), name='deposit'),
    path('withdrawal/', views.WithdrawalCreateView.as_view(), name='withdrawal'),
    path('accounts/list/', views.TransactionListView.as_view(), name='accounts_list'),
]