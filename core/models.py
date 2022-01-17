
import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class TimestampedModel(models.Model):
  # A timestamp representing when this object was created.
  created_at = models.DateTimeField(auto_now_add=True)
  # A timestamp reprensenting when this object was last updated.
  updated_at = models.DateTimeField(auto_now=True)
  class Meta:
    abstract = True
    # By default, any model that inherits from `TimestampedModel` should
    # be ordered in reverse-chronological order. We can override this on a
    # per-model basis as needed, but reverse-chronological is a good
    # default ordering for most models.
    ordering = ['-created_at', '-updated_at']


def recipe_image_file_path(instance, filename):
  """Generate file path for new recipe image"""
  ext = filename.split('.')[-1]
  filename = f'{uuid.uuid4()}.{ext}'

  return os.path.join('uploads/recipe/', filename)

class UserManager(BaseUserManager):

  def create_user(self, email, password=None, **extra_fields):
    """Creates and saves a new user"""
    if not email:
      raise ValueError('Email field is required.')
    user = self.model(email=self.normalize_email(email), **extra_fields)
    user.set_password(password)
    user.save(using=self._db)

    return user

  def create_superuser(self, email, password):
    """Creates and saves a new user"""
    user = self.create_user(email, password)
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)

    return user

class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'



class Tag(TimestampedModel):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class Ingredient(TimestampedModel):
    """Ingredient to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Recipe(TimestampedModel):
  """Recipe object"""
  user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE
  )
  title = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=5, decimal_places=2)
  time_minutes = models.IntegerField()
  link = models.CharField(max_length=255, blank=True)
  tags = models.ManyToManyField('Tag')
  ingredients = models.ManyToManyField('Ingredient')
  image = models.ImageField(upload_to=recipe_image_file_path, null=True)
  
  def _str_(self):
    return self.title