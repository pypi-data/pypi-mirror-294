# Generated by Django 4.2.15 on 2024-08-20 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("metenox", "0002_alter_moon_value"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="general",
            options={
                "default_permissions": (),
                "managed": False,
                "permissions": (
                    ("basic_access", "Can access this app"),
                    (
                        "auditor",
                        "Can access metenox information about all corporations",
                    ),
                ),
            },
        ),
    ]
