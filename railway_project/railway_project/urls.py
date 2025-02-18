# railway_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# A simple home view
def home(request):
    return HttpResponse("Welcome to the Railway Management API!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),  # This will catch the root URL
    path('api/', include('railway.urls')),
]
