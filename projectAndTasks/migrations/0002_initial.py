# Generated by Django 4.0.5 on 2022-08-17 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userMgmt', '0001_initial'),
        ('projectAndTasks', '0001_initial'),
        ('costEstimation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='user_project_map',
            name='project_role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userMgmt.designation'),
        ),
        migrations.AddField(
            model_name='user_project_map',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='taskhierarchy',
            name='parent_task_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_task', to='projectAndTasks.task'),
        ),
        migrations.AddField(
            model_name='taskhierarchy',
            name='sub_task_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_task', to='projectAndTasks.task'),
        ),
        migrations.AddField(
            model_name='taskcomments',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectAndTasks.task'),
        ),
        migrations.AddField(
            model_name='task',
            name='category_id',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='costEstimation.funccategory'),
        ),
        migrations.AddField(
            model_name='task',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectAndTasks.project'),
        ),
        migrations.AddField(
            model_name='project_category_map',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='costEstimation.funccategory'),
        ),
        migrations.AddField(
            model_name='project_category_map',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectAndTasks.project'),
        ),
    ]