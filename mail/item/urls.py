
from django.urls import path

from . import views

# creating a namespace for app
app_name = 'item'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('new/', views.new, name='new'),
    path('', views.browse, name='browse'),
] 
