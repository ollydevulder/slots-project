from django.urls import path

from . import views

app_name = 'slots'
urlpatterns = [
    path('', views.index_view, name='index'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    path('shops/', views.ShopsView.as_view(), name='shops'),
    path('shops/<int:pk>/', views.ShopView.as_view(), name='view-shop'),
    path('shops/<int:shop>/<str:method>/<int:slot>/',
        views.slot_manage_view,
        name='manage-slot'
    ),
    path('shops/<int:shop>/modify/', views.modify_view, name='modify'),

    path('me/', views.user_view, name='user'),
    path('me/slots/', views.SlotsView.as_view(), name='slots'),
    path('me/settings/', views.user_settings_view, name='settings'),
]
