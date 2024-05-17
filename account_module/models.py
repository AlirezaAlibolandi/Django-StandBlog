from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=300, blank=True, null=True, verbose_name='Bio', help_text="It's about you.")
    profile_pic = models.ImageField(upload_to='Profile-pics/', blank=True, null=True, verbose_name='Profile')
    national_code = models.CharField(max_length=10,null=True, blank=True, verbose_name='National Code')
    father_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Father Name')

    def __str__(self):
        return self.user.username