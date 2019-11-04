# Generated by Django 2.2.6 on 2019-11-04 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank_loan_app', '0002_auto_20191103_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Alert_Date', models.DateField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank_loan_app.ProfileData')),
            ],
        ),
    ]
