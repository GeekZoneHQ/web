# Generated by Django 3.1.7 on 2021-04-19 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("memberships", "0012_auto_20210413_1903"),
    ]

    operations = [
        migrations.AddField(
            model_name="membership",
            name="payment_status",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
