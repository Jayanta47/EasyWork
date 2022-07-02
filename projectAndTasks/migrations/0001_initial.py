# Generated by Django 4.0.5 on 2022-07-02 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userMgmt', '0002_designation_alter_user_job_delete_roles'),
        ('costEstimation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='Project', max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('allocated_time', models.IntegerField(default=None, null=True)),
                ('budget', models.IntegerField(default=1000, null=True)),
                ('dev_type', models.CharField(default=None, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='title', max_length=200, null=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateField(default=None, null=True)),
                ('end_time', models.DateField(default=None, null=True)),
                ('slack_time', models.IntegerField(default=0, null=True)),
                ('status', models.CharField(choices=[('C', 'completed'), ('O', 'ongoing'), ('P', 'postponed'), ('U', 'not started')], max_length=2)),
                ('category_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='costEstimation.funccategory')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectAndTasks.project')),
            ],
        ),
        migrations.CreateModel(
            name='User_Project_Map',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField(default=None)),
                ('duration', models.IntegerField(default=None)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectAndTasks.project')),
                ('project_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userMgmt.designation')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userMgmt.user')),
            ],
        ),
        migrations.CreateModel(
            name='TaskHierarchy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('parent_task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_task', to='projectAndTasks.task')),
                ('sub_task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_task', to='projectAndTasks.task')),
            ],
        ),
    ]
