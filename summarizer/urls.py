from django.urls import path
from . import views  # import views from the current directory

# This is where we define the URL patterns for the 'summarizer' app
urlpatterns = [
    # The empty string '' means the root URL (e.g., http://127.0.0.1:8000/)
    # It will be handled by the 'summarize_view' function in views.py
    path('', views.summarize_view, name='home'),
]