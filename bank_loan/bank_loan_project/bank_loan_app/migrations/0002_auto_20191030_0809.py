# Generated by Django 2.2.6 on 2019-10-30 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank_loan_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loandata',
            old_name='Loan_amount',
            new_name='loan_amount',
        ),
    ]
