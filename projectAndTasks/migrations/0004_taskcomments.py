# Generated by Django 4.0.5 on 2022-07-17 03:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectAndTasks', '0003_task_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskComments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=1000)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectAndTasks.task')),
            ],
        ),
    ]
