from django.urls import path
from . import views

urlpatterns=[
	path('register/', views.UserRegistrationAPIView.as_view()),
	path('login/', views.UserLoginAPIView.as_view()),
    path('accounts/login/?next=/swagger/',views.UserLoginAPIView.as_view()),
	path('', views.UserViewAPI.as_view()),
	path('logout/', views.UserLogoutViewAPI.as_view()),]