from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.chat, name='chat'),
    # path('history/', views.chat_history, name='chat_history'),
]
