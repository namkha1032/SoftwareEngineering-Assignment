# Generated by Django 4.1.3 on 2022-11-12 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_transportation_name_alter_transportation_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportation',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transportation',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
