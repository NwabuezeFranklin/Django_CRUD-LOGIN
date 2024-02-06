from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('registerFirst/', views.registerFirst, name="registerFirst"),
    
    path('', views.index, name='index'),
    path('room/<str:pk>/', views.room, name='room'),
    
    
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    
    
    path('create-room', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete/<str:pk>/', views.delete, name="delete"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    
    path('logout/', views.logoutUser, name="logout"),
    
    
]