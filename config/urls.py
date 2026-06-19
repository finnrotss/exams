from django.contrib import admin
from django.urls import include, path

from posts.views import ping_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ping/', ping_view, name='ping'),
    path('', include('clients.urls')),
    #path('', include('books.urls')),
]
