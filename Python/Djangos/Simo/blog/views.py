from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CategoryForm, PostForm
from .models import Category, Post


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.posts.order_by("-created_datetime")
    return render(
        request, "blog/category_detail.html", {"category": category, "posts": posts}
    )


def author_detail(request, pk):
    User = get_user_model()
    author = get_object_or_404(User, pk=pk)
    posts = author.posts.order_by("-created_datetime")
    return render(
        request, "blog/author_detail.html", {"author": author, "posts": posts}
    )


class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    ordering = ["-created_datetime"]
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().order_by("name")
        context["active_category"] = self.request.GET.get("category")
        return context


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post updated successfully!")
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
        messages.success(self.request, "Post deleted successfully!")
        return super().delete(request, *args, **kwargs)


class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.object.posts.order_by("-created_datetime")
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "blog/category_form.html"
    success_url = "/categories/"


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "blog/category_form.html"
    success_url = "/categories/"


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "blog/category_confirm_delete.html"
    success_url = "/categories/"
