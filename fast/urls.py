from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import  SignupView, LoginView
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # API Endpoints
    path('signup/', views.SignupView.as_view(), name='api_signup'),
    path('login/', views.LoginView.as_view(), name='api_login'),
    path('calc-variation/', views.calc_variation, name='calc_variation'),
    path('filter/', views.charts_generation_on_teg, name='charts_generation_on_teg'),
    # HTML Endpoints
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('form/signup/', views.signup_page, name='signup'),
    path('/', views.home_page, name='home_page'),  
    path('form/login/', views.login_page, name='login'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
     path('calc-variation/', views.calc_variation, name='calc_variation_rates'),
    path('download-variation/<str:file_name>/', views.download_variation_file, name='download_variation_file'),
    # User management endpoints
    # path('api/admin/users/', views.UserListCreateAPIView.as_view(), name='user-list-create'),
    # path('api/admin/users/<int:pk>/', views.UserDetailAPIView.as_view(), name='user-detail'),
    path('process-folder/', views.process_folder, name='process_folder'),
    path('download/<str:filename>/', views.download_file, name='download_file'),
]
