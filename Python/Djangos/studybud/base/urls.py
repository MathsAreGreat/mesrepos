from django.urls import path

from .views import (
    ChapterCreateView,
    ChapterDeleteView,
    ChapterUpdateView,
    ChapterListView,
    ChapterDetailView,
    ClasseCreateView,
    ClasseUpdateView,
    ClasseDetailView,
    DomaineCreateView,
    DomaineUpdateView,
    LevelCreateView,
    PostCreateView,
    PostListView,
    PostUpdateView,
    PostDetailView,
    SemesterCreateView,
)


urlpatterns = [
    # Post
    path("", PostListView.as_view(), name="home"),
    path("create-post/", PostCreateView.as_view(), name="create-post"),
    path("update-post/<str:pk>", PostUpdateView.as_view(), name="update-post"),
    path("post/<str:pk>", PostDetailView.as_view(), name="post-detail"),
    # Level
    path("create-level/", LevelCreateView.as_view(), name="create-level"),
    # Chapter
    path("chapter/<str:pk>", ChapterDetailView.as_view(), name="chapter-detail"),
    path("create-chapter/", ChapterCreateView.as_view(), name="create-chapter"),
    path("update-chapter/<str:pk>", ChapterUpdateView.as_view(), name="update-chapter"),
    # Classe
    path("classe/<str:pk>", ClasseDetailView.as_view(), name="classe-detail"),
    path("create-classe/", ClasseCreateView.as_view(), name="create-classe"),
    path("update-classe/<str:pk>", ClasseUpdateView.as_view(), name="update-classe"),
    # Semester
    path("create-semester/", SemesterCreateView.as_view(), name="create-semester"),
    # Domaine
    path("create-domaine/", DomaineCreateView.as_view(), name="create-domaine"),
    path("update-domaine/<str:pk>", DomaineUpdateView.as_view(), name="update-domaine"),
]
