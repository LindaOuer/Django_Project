# Generated by Django 3.0.4 on 2020-03-31 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectName', models.CharField(max_length=30, verbose_name='Titre du projet')),
                ('projectDuration', models.IntegerField(default=0, verbose_name='Duree estimee')),
                ('timeAllocated', models.IntegerField(verbose_name='Temps alloue')),
                ('needs', models.TextField(max_length=250)),
                ('description', models.TextField(max_length=250)),
                ('isValid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastName', models.CharField(max_length=30, verbose_name='Prenom')),
                ('firstName', models.CharField(max_length=30, verbose_name='Nom')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
            ],
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hub.User')),
            ],
            bases=('hub.user',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hub.User')),
            ],
            bases=('hub.user',),
        ),
        migrations.CreateModel(
            name='MembershipInProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_allocated_by_member', models.IntegerField(verbose_name='Temps alloué par le membre')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hub.Project')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hub.Student')),
            ],
            options={
                'unique_together': {('project', 'student')},
            },
        ),
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='project_owner', to='hub.Student'),
        ),
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='les_membres', through='hub.MembershipInProject', to='hub.Student'),
        ),
        migrations.AddField(
            model_name='project',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_coach', to='hub.Coach'),
        ),
    ]