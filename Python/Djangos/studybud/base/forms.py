from django import forms

from .models import Chapter, Classe, Domaine, Level, Post, Semester

import re


class LevelForm(forms.ModelForm):
    title = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Saisir le titre du niveau ..",
            }
        ),
    )

    class Meta:
        model = Level
        fields = ["title"]

    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        cn = title.split(" ")
        return " ".join(e.strip().title() for e in cn if e.strip())


class DomaineForm(forms.ModelForm):
    title = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Saisir le titre du domaine ..",
            }
        ),
    )

    class Meta:
        model = Domaine
        fields = ["title"]

    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        cn = title.split(" ")
        return " ".join(e.strip().title() for e in cn if e.strip())


class ClasseForm(forms.ModelForm):
    title = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Saisir le titre de la classe ..",
            }
        ),
    )
    name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Saisir le nom complet de la classe ..",
            }
        ),
    )
    level = forms.ModelChoiceField(
        queryset=Level.objects.all().order_by("title"),
        label="",
        empty_label=" -- Sélectionner un niveau -- ",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    year = forms.IntegerField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Classe
        fields = ["title", "year", "name", "level"]

    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        cn = title.split(" ")
        return " ".join(e.strip().upper() for e in cn if e.strip())

    def clean_name(self):
        title = self.cleaned_data.get("name", "")
        cn = title.split(" ")
        return " ".join(e.strip().title() for e in cn if e.strip())


class SemesterForm(forms.ModelForm):
    title = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Saisir le titre du semestre ..",
            }
        ),
    )

    class Meta:
        model = Semester
        fields = ["title"]

    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        cn = title.split(" ")
        return " ".join(e.strip().title() for e in cn if e.strip())


class ChapterForm(forms.ModelForm):
    title = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Saisir le titre du niveau ..",
            }
        ),
    )
    domaine = forms.ModelChoiceField(
        queryset=Domaine.objects.all().order_by("title"),
        label="",
        empty_label=" -- Sélectionner un domaine -- ",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )
    classe = forms.ModelChoiceField(
        queryset=Classe.objects.all().order_by("year"),
        label="",
        empty_label=" -- Sélectionner une classe -- ",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    semester = forms.ModelChoiceField(
        queryset=Semester.objects.all().order_by("title"),
        label="",
        empty_label=" -- Sélectionner une semester -- ",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Chapter
        fields = ["title", "domaine", "classe", "semester"]

    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        cn = title.split(" ")
        return " ".join(e.strip().title() for e in cn if e.strip())


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Saisir le titre de l'article ..",
            }
        ),
    )
    description = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Saisir une description de l'article ..",
            }
        ),
    )
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "rows": 8,
                "placeholder": "Saisir le contenu de l'article ..",
                "class": "form-control",
            }
        ),
    )
    chapter = forms.ModelChoiceField(
        queryset=Chapter.objects.all().order_by("title"),
        label="",
        empty_label=" -- Sélectionner un chapitre -- ",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Post
        fields = ["title", "description", "content", "chapter"]

    def clean_description(self):
        title = self.cleaned_data.get("description", "")
        cn = title.split(" ")
        cn = [e.strip() for e in cn if e.strip()]
        cn[0] = cn[0].capitalize()
        return " ".join(cn)

    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        cn = title.split(" ")
        return " ".join(e.strip().title() for e in cn if e.strip())

    def clean_content(self):
        title = self.cleaned_data.get("content", "")
        cn = title.split("\n")
        return " ".join(re.sub(r"<!-[^>]+>", r"", e.strip()) for e in cn if e.strip())
