# Generated by Django 4.0.5 on 2022-08-21 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('job_name', models.CharField(default=None, max_length=100)),
                ('salary', models.IntegerField(default=0)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('salary_valid_till', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('email', models.EmailField(default=None, max_length=254, unique=True)),
                ('mobile', models.CharField(default=None, max_length=15, null=True)),
                ('address', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('date_of_birth', models.DateField(blank=True, default=None, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'MALE'), ('F', 'FEMALE'), ('O', 'OTHER')], default=None, max_length=1, null=True)),
                ('joining_date', models.DateField(auto_now_add=True)),
                ('job', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userMgmt.designation')),
            ],
        ),
    ]
