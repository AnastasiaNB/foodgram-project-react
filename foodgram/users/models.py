from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    username = models.CharField(verbose_name='Логин', unique=True, max_length=20)
    password = models.CharField(verbose_name='Пароль', max_length=10)
    email = models.EmailField(verbose_name='email')
    first_name = models.CharField(verbose_name='Имя', max_length=15)
    last_name = models.CharField(verbose_name='Фамилия', max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
