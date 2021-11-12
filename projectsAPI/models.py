from django.db import models
from django.utils.translation import gettext_lazy as _


# Keyword Model
class Keyword(models.Model):
    word = models.CharField(max_length=64, unique=True)
    date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.date} - {self.word}"

# Project Model
class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    duration = models.IntegerField(help_text="Integer in months")
    description = models.TextField()
    keywords = models.ManyToManyField(Keyword)

    class Meta:
        ordering = ['-date']

    def __str__(self) -> str:
        return f"{self.date} - {self.name}"
