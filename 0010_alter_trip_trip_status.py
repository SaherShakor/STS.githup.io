# Generated by Django 4.2.6 on 2024-02-24 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sts', '0009_trip_trip_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='trip_status',
            field=models.CharField(blank=True, choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], max_length=32, null=True),
        ),
    ]
