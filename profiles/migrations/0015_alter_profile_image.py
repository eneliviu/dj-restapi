# Generated by Django 5.1.3 on 2024-12-01 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../sample', upload_to='images/'),
        ),
    ]
