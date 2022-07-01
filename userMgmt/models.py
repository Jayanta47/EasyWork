from django.db import models

# Create your models here.


# Roles and salary

class Roles(models.Model):
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
        default = 1000,
        null=False
    )

    date_created = models.DateField(
        auto_now_add=True,
        null=False
    )

    valid_till = models.DateField(
        default=None,
        blank=True,
        null=True
    )

    


# USER 

class User(models.Model):

    GENDER_LIST = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'OTHER')
    ]

    id = models.AutoField(
        primary_key=True
    )

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
        Roles,
        default=None,
        on_delete=models.SET_NULL,
        null=True
    )


    joining_date = models.DateField(
        auto_now_add=True,
        blank=True,
        null=False
    )


