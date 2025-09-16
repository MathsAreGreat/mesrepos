from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    DetailView,
)
from django.core.paginator import Paginator

from .forms import (
    ChapterForm,
    ClasseForm,
    DomaineForm,
    LevelForm,
    PostForm,
    SemesterForm,
)
from .models import Chapter, Classe, Domaine, Level, Post, Semester


# Domaine area routes
class DomaineListView(ListView):
    model = Domaine

    ordering = ["-created_datetime"]
    context_object_name = "domaines"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Liste des domaines"
        return context


class DomaineCreateView(LoginRequiredMixin, CreateView):
    model = Domaine
    form_class = DomaineForm
    template_name = "base/main_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Créer un nouveau domaine"
        context["items"] = Domaine.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Domaine créé avec succès!")
        return super().form_valid(form)


class DomaineUpdateView(LoginRequiredMixin, UpdateView):
    model = Domaine
    form_class = DomaineForm
    template_name = "base/main_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Modifier un domaine"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Domaine modifié avec succès!")
        return super().form_valid(form)


# Level area routes
class LevelListView(ListView):
    model = Level
    ordering = ["-created_datetime"]
    context_object_name = "levels"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Liste des niveaux"
        return context


class LevelCreateView(LoginRequiredMixin, CreateView):
    model = Level
    form_class = LevelForm
    template_name = "base/main_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Créer un nouveau niveau"
        context["items"] = Level.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Niveau créé avec succès!")
        return super().form_valid(form)


# Chapter area routes
class ChapterListView(ListView):
    model = Chapter
    ordering = ["-created_datetime"]
    context_object_name = "chapters"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Liste des chapitres"
        return context


class ChapterCreateView(LoginRequiredMixin, CreateView):
    model = Chapter
    form_class = ChapterForm
    template_name = "base/main_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Créer un nouveau chapitre"
        context["items"] = Chapter.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Chapitre créé avec succès!")
        return super().form_valid(form)


class ChapterUpdateView(UpdateView):
    model = Chapter
    form_class = ChapterForm
    template_name = "base/main_form.html"
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, "Chapitre mis à jour avec succès!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Modifier le chapitre"
        return context


class ChapterDeleteView(DeleteView):
    model = Chapter
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Chapitre supprimé avec succès!")
        return super().delete(request, *args, **kwargs)


class ChapterDetailView(DetailView):
    model = Chapter
    template_name = "base/chapter_detail.html"
    context_object_name = "chapter"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter = self.get_object()

        # Get all posts for this chapter, ordered by creation date
        posts = Post.objects.filter(chapter=chapter).order_by("-created_datetime")

        # Paginate posts
        paginator = Paginator(posts, 6)  # 6 posts per page
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["posts"] = page_obj
        context["total_posts"] = posts.count()
        context["is_paginated"] = paginator.num_pages > 1

        return context


# Classe area routes
class ClasseListView(ListView):
    model = Classe
    ordering = ["-created_datetime"]
    context_object_name = "classes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Liste des classes"
        return context


class ClasseDetailView(DetailView):
    model = Classe
    template_name = "base/classe_detail.html"
    context_object_name = "classe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classe = self.get_object()
        # All chapters in this class
        chapters = Chapter.objects.filter(classe=classe).order_by("title")
        context["chapters"] = chapters
        # Optionally, all posts in this class (across all chapters)
        posts = Post.objects.filter(chapter__classe=classe).order_by(
            "-created_datetime"
        )
        context["posts"] = posts
        context["total_posts"] = posts.count()
        return context


class ClasseCreateView(LoginRequiredMixin, CreateView):
    model = Classe
    form_class = ClasseForm
    template_name = "base/main_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Créer une nouvelle classe"
        context["items"] = Classe.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Classe créée avec succès!")
        return super().form_valid(form)


class ClasseUpdateView(UpdateView):
    model = Classe
    form_class = ClasseForm
    template_name = "base/main_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Classe modifiée avec succès!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Modifier la classe"
        return context


class ClasseDeleteView(DeleteView):
    model = Classe
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Classe supprimée avec succès!")
        return super().delete(request, *args, **kwargs)


# Semester area routes
class SemesterListView(ListView):
    model = Semester
    ordering = ["-created_datetime"]
    context_object_name = "semesters"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Liste des semestres"
        return context


class SemesterCreateView(LoginRequiredMixin, CreateView):
    model = Semester
    form_class = SemesterForm
    template_name = "base/main_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Créer un nouveau semestre"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Semestre créé avec succès!")
        return super().form_valid(form)


class SemesterUpdateView(UpdateView):
    model = Semester
    form_class = SemesterForm
    template_name = "base/main_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Semestre modifié avec succès!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Modifier le semestre"
        return context


class SemesterDeleteView(DeleteView):
    model = Semester
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Semestre supprimé avec succès!")
        return super().delete(request, *args, **kwargs)


# Post area routes
class PostListView(ListView):
    model = Post
    ordering = ["-created_datetime"]
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(chapter_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Chapter.objects.all().order_by("title")
        context["active_category"] = self.request.GET.get("category")
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "base/main_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Créer un nouvel article"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Article créé avec succès!")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "base/main_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Article modifié avec succès!")
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Article supprimé avec succès!")
        return super().delete(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = "base/post_detail.html"
    context_object_name = "post"
