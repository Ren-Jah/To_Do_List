# Generated by Django 4.0.1 on 2022-12-28 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='description',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='due_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Дата выполнения'),
        ),
    ]
