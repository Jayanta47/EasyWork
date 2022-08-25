# Generated by Django 4.0.5 on 2022-08-21 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userMgmt', '0001_initial'),
        ('projectAndTasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Milestones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='User_Task_Map',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('assign_date', models.DateField(auto_now_add=True, null=True)),
                ('duration', models.IntegerField(default=None, null=True)),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectAndTasks.task')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userMgmt.user')),
            ],
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dependent_on_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depending_task', to='projectAndTasks.task')),
                ('parent_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_of_dependent_task', to='projectAndTasks.task')),
            ],
        ),
    ]