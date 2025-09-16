"""
URL configuration for school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from . import views
from .views import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryDetailView,
    CategoryListView,
    CategoryUpdateView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="home"),  # Main homepage
    path("post/new/", PostCreateView.as_view(), name="create_post"),
    path("post/<int:pk>/update", PostUpdateView.as_view(), name="update_post"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("posts/", PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="delete_post"),
    path("category/new/", CategoryCreateView.as_view(), name="create_category"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("category/<int:pk>/edit/", CategoryUpdateView.as_view(), name="edit_category"),
    path(
        "category/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="delete_category",
    ),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("author/<int:pk>/", views.author_detail, name="author_detail"),
]
