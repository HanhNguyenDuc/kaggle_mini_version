
from django.contrib.auth import views as auth_view
from django.urls import path
from .views import RegisterView, get_home_page, get_contest, get_info_page, upload_file, upload_file_2

urlpatterns = [
    path(r'registration/', RegisterView.as_view(), name='register'),
    path(r'login/', auth_view.LoginView.as_view(template_name='home/login.html')),
    path(r'logout/', auth_view.LogoutView.as_view(), name='logout'),
    path(r'', get_home_page, name='home'),
    path(r'contest/<int:id>', get_contest, name = 'contest'),
    path(r'info/', get_info_page, name='info'),
    path(r'upload_demo/', upload_file, name='upload'),
    path(r'upload_demo_2/', upload_file_2, name="upload2")
]