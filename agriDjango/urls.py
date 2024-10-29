from django.contrib import admin
from django.urls import path
from climate import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('template/tables', views.template_tables, name='template_tables'),

    path('admin/', admin.site.urls),

    # Weather URL
    path('weather/', views.index, name='weather'),

    # Fields URLs
    path('fields/create/', views.create_field, name='create_field'),
    path('fields/', views.field_list, name='field_list'),
    path('fields/<int:field_id>/delete/', views.field_delete, name='field_delete'),
    path('fields/<int:field_id>/update/', views.field_update, name='field_update'),

    # Water Sources URLs
    path('water_sources/create/', views.create_water_source, name='create_water_source'),
    path('water_sources/', views.water_source_list, name='water_source_list'),
    path('water_sources/<int:water_source_id>/delete/', views.water_source_delete, name='water_source_delete'),
    path('water_sources/<int:water_source_id>/update/', views.water_source_update, name='water_source_update'),

    # Water Usage URLs
    path('water_usages/create/', views.create_water_usage, name='create_water_usage'),
    path('water_usages/', views.water_usage_list, name='water_usage_list'),
    path('water_usages/<int:water_usage_id>/delete/', views.water_usage_delete, name='water_usage_delete'),
    path('water_usages/<int:water_usage_id>/update/', views.water_usage_update, name='water_usage_update'),

    # Prediction URL

    path('predict/',views.predict_water_usage, name='predict_water_usage'),  # Assurez-vous que c'est correct


]
