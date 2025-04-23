from django.db import models
from account.models import Account

# Create your models here.

def user_directory_path(instance, filename):
    return f'user_{instance.user.username}/{filename}'

class Image(models.Model):
    title = models.CharField(max_length=75)
    image = models.ImageField(upload_to=user_directory_path)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.title