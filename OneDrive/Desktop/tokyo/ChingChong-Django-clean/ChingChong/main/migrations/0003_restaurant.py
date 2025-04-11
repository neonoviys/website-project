# Generated by Django 4.2.18 on 2025-01-26 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_cities_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress', models.CharField(blank=True, max_length=256, null=True, verbose_name='Адресс')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cities')),
            ],
            options={
                'verbose_name': 'restaurant',
                'verbose_name_plural': 'Restaurants',
            },
        ),
    ]
