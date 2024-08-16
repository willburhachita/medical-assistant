from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('challenge/', views.SignatureView.as_view()),
    path('current/', views.CurrentUserView.as_view()),
    path('<int:pk>/', views.AccountView.as_view(), name='account-detail'),
    path('all-users/', views.AllUsersView.as_view(), name='all-users'),
    path('', views.AccountView.as_view(), name='account-creation'),
]
