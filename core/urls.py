from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name='login'), # Create the log in path
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Create the logout path
    path('custom_redirect/', custom_redirect_view, name='custom_redirect'), # URL for redirecting user based on role
    path('trainee_view/', trainee_view, name='trainee_view'),  # Trainee ITP records
    path('trainer/', trainer_view, name='trainer_view'), # Trainer view
    path('supervisor_view/', supervisor_view, name='supervisor_view'),
    path('create_form/', create_form_view, name='create_form'), # ITP creation form path
    path('add_tasks/', add_tasks, name='add_tasks'),
    path('edit_user/<user_id>/', edit_user_view, name='edit_user_info')
]