# Generated by Django 2.2.6 on 2019-10-30 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_loan_app', '0004_auto_20191030_0813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loandata',
            name='status',
        ),
        migrations.AddField(
            model_name='loandata',
            name='Status',
            field=models.BooleanField(default=False),
        ),
    ]
