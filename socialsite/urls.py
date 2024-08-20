from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('room/<int:pk>/', views.room, name = 'room' ),

    path('update-room/<int:pk>/', views.updateroom, name='update'),

    path('delete/<int:pk>/', views.delete, name='delete'),

    path('login/', views.loginPage, name='login'),

    path('register/', views.registerPage, name='register'),

    path('logout/', views.logoutuser, name='logout'),
    
    path('create-room/', views.createroom, name='create-room'),

    path('delete_message/<int:pk>/', views.deleteMessage, name="delete_message"),

    path('profile/<str:pk>/', views.userProfile, name='profiles'),

    path('editprofile/<str:pk>/', views.editProfile, name='editprofile'),
]
