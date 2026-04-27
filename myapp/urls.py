from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('insert/', views.insertdata, name='insert'),
    path('update/<int:id>/', views.updatedata, name='updatedata'),
    path('delete/<int:id>/', views.deletedata, name='deletedata'),
]

 
