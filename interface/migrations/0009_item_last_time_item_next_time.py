# Generated by Django 5.0.4 on 2024-10-11 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0008_item_area_item_aspect_item_branch_item_field_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='last_time',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='next_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]
