from django.urls import path
from . import views


urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('comments/', views.comment_list),
    path('articles/<int:article_pk>/comments/', views.comment_create),
    path('articles/<int:article_pk>/<int:comment_pk>/delete/', views.comment_delete),
    
]
