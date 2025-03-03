from django.contrib.auth.models import AbstractUser  # AbstractUser'ı import edin
from django.db import models

class CustomUser(AbstractUser):
    # Eğer ek alanlar eklemek istiyorsanız buraya ekleyebilirsiniz
    pass

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    reset_code = models.CharField(max_length=6, blank=True, null=True)

