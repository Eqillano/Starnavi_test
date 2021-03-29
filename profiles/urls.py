from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, LoginView, TokenAuthenticationView, ProfileView, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('last-activity/', TokenAuthenticationView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', ProfileView.as_view(), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout')
]
