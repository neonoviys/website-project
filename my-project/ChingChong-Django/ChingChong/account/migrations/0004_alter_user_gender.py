# Generated by Django 4.2.18 on 2025-01-26 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский'), ('D', '...')], default='D', max_length=10, verbose_name='Sex'),
        ),
    ]
