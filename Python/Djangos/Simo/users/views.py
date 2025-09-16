from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, RedirectView

from blog.models import Post


# Signup View
class SignupView(SuccessMessageMixin, FormView):
    template_name = "users/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    success_message = "Welcome to StudentBlog, %(username)s!"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.success_message = self.success_message % {"username": user.username}
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


# Login View
class LoginView(SuccessMessageMixin, FormView):
    template_name = "users/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome back, {username}!")
            return super().form_valid(form)
        messages.error(self.request, "Invalid username or password.")
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
    pattern_name = "home"

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have been successfully logged out!")
        return super().get(request, *args, **kwargs)
