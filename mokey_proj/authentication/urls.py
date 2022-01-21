from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name='authentication'

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('activate/<uidb64>/<token>', views.Activate_VerficationEmail, name="Activate_VerficationEmail"),
    # path('naver_register/', csrf_exempt(views.naver_user_register), name='naver_user_register'),
    path('logout/', views.user_logout, name='user_logout'), 

    path('reset-password', views.resetPassword, name='resetPassword'),
    path('set-password/<uidb64>/<token>', views.setPassword, name='setPassword'),
]

