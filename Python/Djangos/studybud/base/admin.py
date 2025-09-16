from django.contrib import admin

from .models import Chapter, Classe, Domaine, Level, Post, Semester

# Register your models here.

admin.site.register(Post)
admin.site.register(Chapter)
admin.site.register(Classe)
admin.site.register(Level)
admin.site.register(Semester)
admin.site.register(Domaine)
