from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.files.storage import FileSystemStorage
# Create your models here.
fs = FileSystemStorage(location='/passport_photograhs')
class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, name, password=None):
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, password):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            password=password,
            name= "True",
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField( unique=True)
    name = models.CharField(max_length=100)
    passport_photograh = models.CharField(max_length=1000)
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.name

