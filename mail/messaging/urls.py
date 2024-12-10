from django.urls import path
from . import views

app_name = 'conversation'

urlpatterns = [
    path('messages/<int:item_pk>/', views.new_conversation, name='conversation'),
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.detail, name='detail'),
]
