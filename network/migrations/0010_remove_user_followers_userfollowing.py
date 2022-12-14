# Generated by Django 4.0.1 on 2022-09-20 21:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_remove_user_following_alter_user_followers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.CreateModel(
            name='UserFollowing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('following_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
