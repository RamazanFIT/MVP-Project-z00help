# Generated by Django 4.2.4 on 2023-08-25 03:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.CreateModel(
            name='OwnAnimal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='animals_images/')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnimalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='animals_images/')),
                ('post_take_animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.ownanimal')),
            ],
        ),
    ]