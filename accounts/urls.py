from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change/password/', views.change_password, name='change_password'),
    path('password/reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', views.UserPasswordResetDone.as_view(), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]
