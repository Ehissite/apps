from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import LoginForm

# can be used to locate the url
app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
]
