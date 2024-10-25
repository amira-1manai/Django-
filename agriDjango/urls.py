from django.contrib import admin
from django.urls import path
from climate import views
from django.urls import path

urlpatterns = [
    path('', views.home_view, name='home'),
    path('template/tables', views.template_tables, name='home'),

    path('admin/', admin.site.urls),


    path('weather/', views.index, name='weather'),

    #fields
    path('fields/create/', views.create_field, name='create_field'),
    path('fields/', views.field_list, name='field_list'),
    path('fields/<int:field_id>/delete/', views.field_delete, name='field_delete'),
    path('fields/<int:field_id>/update/', views.field_update, name='field_update'),  # Update URL
    
    
    
    #crop 
    path('crop/create/', views.create_crop, name='create_crop'),
    path('crops/', views.crop_list, name='crop_list'),
    path('update-crop/<int:crop_id>/', views.crop_update, name='crop_update'),
    path('delete-crop/<int:crop_id>/', views.delete_crop, name='crop_delete'),
]
