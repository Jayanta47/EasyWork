# Generated by Django 4.0.5 on 2022-08-27 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FuncCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, null=True)),
                ('expected_time', models.IntegerField(default=0, null=True)),
                ('man_hour_per_week', models.IntegerField(default=0, null=True)),
                ('allocated_budget', models.IntegerField(default=0, null=True)),
                ('loc', models.IntegerField(default=0, null=True)),
                ('loc_per_pm', models.FloatField(default=0.0, null=True)),
                ('cost_per_loc', models.IntegerField(default=0, null=True)),
                ('difficulty', models.CharField(choices=[('E', 'easy'), ('M', 'medium'), ('H', 'hard')], default='E', max_length=15)),
                ('estimated_cost', models.IntegerField(default=0, null=True)),
                ('misc_cost', models.IntegerField(default=0, null=True)),
            ],
        ),
    ]
