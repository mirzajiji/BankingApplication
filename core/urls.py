from core import admin
from core.views.root import api_root
from core.views.user_views import register_user, user_to_user_transaction, get_account_balance, get_user_transactions
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views.admin_views import admin_add_balance


urlpatterns = [
    path('', api_root, name='api-root'),
    path('login/', TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('register/',register_user,name='register'),
    path('token/refresh/', TokenRefreshView.as_view(),name='token_refresh'),
    path('admin/add-balance/', admin_add_balance, name='admin_add_balance'),
    path('transfer/',  user_to_user_transaction, name='user_to_user_transaction'),
    path('balance/',get_account_balance, name='get_account_balance'),
    path('transactions/', get_user_transactions, name='get_transactions'),
]