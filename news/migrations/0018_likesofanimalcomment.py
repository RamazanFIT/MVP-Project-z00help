# Generated by Django 4.2.4 on 2023-08-26 02:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0017_comment_likes_likesoftakeanimalcomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikesOfAnimalComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bolean', models.BooleanField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.commentforownanimal')),
            ],
        ),
    ]