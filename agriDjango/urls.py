from django.contrib import admin
from django.urls import path
from climate import views, ai

urlpatterns = [
    path('', views.home_view, name='home'),
    path('template/tables', views.template_tables, name='home'),

    path('admin/', admin.site.urls),


    # path('weather/', views.fetch_weather_data, name='weather'),
    path('weather/', views.fetch_weather_data, name='fetch_weather_data'),
    path('ai/', ai.ai, name='ai'),


    #fields
    path('fields/create/', views.create_field, name='create_field'),
    path('fields/', views.field_list, name='field_list'),
    path('fields/<int:field_id>/delete/', views.field_delete, name='field_delete'),
    path('fields/<int:field_id>/update/', views.field_update, name='field_update'),  # Update URL
]
