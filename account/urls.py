from django.urls import include, path
from .apis import LoginView, LogoutView, GetUserInfoView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get_user_info/', GetUserInfoView.as_view(), name='get_user_info'),
]
