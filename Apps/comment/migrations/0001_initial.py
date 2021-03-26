# Generated by Django 3.1.7 on 2021-03-25 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('job', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentary', models.TextField(verbose_name='Commentary')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is activated ?')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('updated_on', models.DateTimeField(auto_now_add=True, verbose_name='Updated on')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='job.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ('user', 'job', 'updated_on'),
            },
        ),
    ]