# Generated by Django 5.1.1 on 2024-12-23 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0007_file_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
