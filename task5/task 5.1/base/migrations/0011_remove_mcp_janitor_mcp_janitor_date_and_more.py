# Generated by Django 4.1.3 on 2022-11-12 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_remove_mcp_janitor_mcp_janitor_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='mcp_janitor',
            name='mcp_janitor_date',
        ),
        migrations.AddConstraint(
            model_name='mcp_collector',
            constraint=models.UniqueConstraint(fields=('collector', 'mcp', 'work_date'), name='mcp_collector_date'),
        ),
        migrations.AddConstraint(
            model_name='mcp_janitor',
            constraint=models.UniqueConstraint(fields=('janitor', 'work_date'), name='mcp_janitor_date'),
        ),
        migrations.AddConstraint(
            model_name='trolley_janitor',
            constraint=models.UniqueConstraint(fields=('janitor', 'work_date'), name='trolley_janitor_date'),
        ),
        migrations.AddConstraint(
            model_name='vehicle_collector',
            constraint=models.UniqueConstraint(fields=('collector', 'work_date'), name='vehicle_collector_date'),
        ),
    ]
