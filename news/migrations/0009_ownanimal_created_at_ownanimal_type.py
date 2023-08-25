# Generated by Django 4.2.4 on 2023-08-25 05:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_rename_post_take_animal_animalimage_animal'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownanimal',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ownanimal',
            name='type',
            field=models.CharField(choices=[('cat', 'кошка'), ('dog', 'собака')], default='cat', max_length=15),
        ),
    ]