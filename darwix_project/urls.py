"""
URL configuration for darwix_project project.
"""
from django.contrib import admin
from django.urls import path, include
from ai_features_app import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ai_features_app.urls')),
    path('', main_views.index, name='index'),  # Serve the frontend
] 