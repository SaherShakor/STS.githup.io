# Generated by Django 4.2.6 on 2024-02-23 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sts', '0005_user_is_active_user_is_staff_user_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Captain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(blank=True, null=True)),
            ],
        ),
    ]
