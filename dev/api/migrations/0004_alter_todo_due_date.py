# Generated by Django 5.1.2 on 2024-10-26 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_todo_created_at_alter_todo_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
