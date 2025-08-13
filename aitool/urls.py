from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('summarizer.urls')),  # Add this line to include your app's URLs
]