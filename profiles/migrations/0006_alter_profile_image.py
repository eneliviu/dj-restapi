# Generated by Django 5.1.4 on 2024-12-28 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='/image/upload/hvc6gc5ikhagzoytuq3k', null=True, upload_to=''),
        ),
    ]