# Generated by Django 4.0.5 on 2022-07-31 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costEstimation', '0003_funccategory_allocated_budget_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funccategory',
            name='allocated_budget',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='funccategory',
            name='expected_time',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
