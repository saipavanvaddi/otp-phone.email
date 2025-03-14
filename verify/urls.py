from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('get_user_info/', views.get_user_info, name='get_user_info'),
    path('save_visitor/', views.save_visitor, name='save_visitor'),
    path('list-flats/', views.list_flats, name='list_flats'),
] 