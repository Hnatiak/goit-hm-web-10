from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .forms import LoginForm

app_name = 'app_auth'

urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='signup'), # app_photo:signup, тепер ідемо в views
    path('signin/', LoginView.as_view(template_name='app_auth/login.html', form_class=LoginForm, redirect_authenticated_user=True), name='signin'), # app_photo:signin, тепер ідемо в views
    path('logout/', views.logout_view, name='logout'), # app_photo:logout, тепер ідемо в views
]