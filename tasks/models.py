from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecomplete = models.DateTimeField(null=True, verbose_name='Fecha completado', blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
