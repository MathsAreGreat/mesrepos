from django import forms

from .models import Category, Post  # Adjust if your model name is different


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "desc",
            "content",
            "category",
        ]  # Add your actual model fields
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter title"}
            ),
            "desc": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter description"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Write your content here...",
                }
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = " -- Select a category -- "

    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        cn = title.split(" ")
        return " ".join(e.strip().title() for e in cn if e.strip())

    def clean_content(self):
        content = self.cleaned_data.get("content", "")
        cn = content.replace("\n", " ").split(" ")
        return " ".join(e.strip() for e in cn if e.strip())


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Category name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description (optional)",
                    "rows": 3,
                }
            ),
        }
