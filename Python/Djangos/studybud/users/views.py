from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, RedirectView, UpdateView

from base.models import Post
from .forms import CustomUserCreationForm, ProfileEditForm


# Signup View
class SignupView(SuccessMessageMixin, FormView):
    template_name = "users/signup.html"
    form_class = CustomUserCreationForm

    success_url = reverse_lazy("users:login")
    success_message = "Bienvenue sur StudentBlog, %(username)s!"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.success_message = self.success_message % {"username": user.username}
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs ci-dessous.")
        return super().form_invalid(form)


# Login View
class LoginView(SuccessMessageMixin, FormView):
    template_name = "users/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("users:profile")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("users:profile")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome back, {username}!")
            return super().form_valid(form)
        messages.error(self.request, "Nom d'utilisateur ou mot de passe incorrect.")
        return self.form_invalid(form)


# Profile View


class ProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "users/profile.html"
    context_object_name = "user_posts"
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by(
            "-created_datetime"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_posts"] = self.get_queryset().count()
        context["is_paginated"] = self.paginate_by < self.get_queryset().count()
        return context


# Logout View
class LogoutView(RedirectView):
    pattern_name = "users:login"

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Vous avez été déconnecté avec succès!")
        return super().get(request, *args, **kwargs)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user
