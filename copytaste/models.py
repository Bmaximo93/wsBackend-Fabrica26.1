from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Recipe(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes') # relação de 1:N com User
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    summary = models.CharField(max_length=255, blank=True)
    ingredients = models.JSONField()
    steps = models.JSONField()
    duration_minutes = models.IntegerField(null=True, blank=True)
    source_url = models.URLField(blank=True, max_length=300) # TODO: ver se 300 é suficiente pra link do youtube
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title