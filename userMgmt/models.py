from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


# Roles and salary

class Designation(models.Model):
    id = models.AutoField(
        primary_key=True
    )

    job_name = models.CharField(
        default = None,
        null = False,
        blank=False,
        max_length=100,
    )

    salary = models.IntegerField(
        default = 0,
        null=False
    )

    date_created = models.DateField(
        auto_now_add=True,
        null=False
    )

    salary_valid_till = models.DateField(
        default=None,
        blank=True,
        null=True
    )

    


# USER 

class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    # def create_user(self, email, password=None, **extra_fields):
    #     """Create and save a regular User with the given email and password."""
    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_superuser', False)
    #     return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password):
        """Create and save a SuperUser with the given email and password."""
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):

    GENDER_LIST = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'OTHER')
    ]

    id = models.AutoField(
        primary_key=True
    )

    username = None

    password = models.CharField(max_length=255, default=None, null=True)

    first_name = models.CharField(
        max_length=200,
        default=None,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        max_length=200,
        default=None,
        blank=True,
        null=True
    )

    email = models.EmailField(
        unique = True,
        default=None,
        blank=False,
        null=False 
    )

    mobile = models.CharField(
        max_length=15,
        default = None,
        null = True  
    )

    address = models.CharField(
        max_length=200,
        default=None,
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        default=None,
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=1,
        default=None,
        blank=True,
        null=True,
        choices = GENDER_LIST 
    )

    job = models.ForeignKey(
        Designation,
        default=None,
        on_delete=models.SET_NULL,
        null=True
    )


    joining_date = models.DateField(
        auto_now_add=True,
        blank=True,
        null=False
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def full_name(self):
        return self.first_name + self.last_name

