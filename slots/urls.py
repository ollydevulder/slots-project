from django.urls import path

from . import views

app_name = 'slots'
urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    path('shops/', views.ShopsView.as_view(), name='shops'),
    path('shops/<int:pk>/', views.ShopView.as_view(), name='view-shop'),
]
