from django.db import models

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=500)
    content = models.CharField(max_length=5000)

    def __str__(self):
        return self.title
    

