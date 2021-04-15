from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(User):
    is_authorized = models.BooleanField(default=False)