from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path('', views.main, name="root"),
    path('authors/', views.authors, name='base'),
    path('<int:page>', views.main, name="root_paginate"),
    path('upload/', views.upload, name='upload'),
    # path('author/edit/<int:pic_id>', views.edit, name='edit'),
    # path('author/delete/<int:pic_id>', views.remove, name='delete'),
]