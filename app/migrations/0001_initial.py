# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-26 08:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctype', models.CharField(choices=[('hospital', 'Hospital'), ('bloodbank', 'Blood Bank'), ('dentalclinic', 'Dental Clinic'), ('pathologylab', 'Pathology Lab'), ('pathologylab2', 'Pathology Lab with Histopathology'), ('clinic', 'Clinic'), ('dispensary', 'Dispensary'), ('vethospital', 'Veterinary Hospital'), ('vetclinic', 'Veterinary Clinic'), ('others', 'Others')], max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='OwnerShipTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otype', models.CharField(choices=[('government', 'Government'), ('semigovernment', 'Semi Government'), ('corporatepublic', 'Corporate Public'), ('corporateprivate', 'Corporate Private'), ('partnership', 'Partnership'), ('individual', 'Individual Owned'), ('others', 'Others')], max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='PrimaryAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='SecondaryAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=64)),
                ('category', models.CharField(max_length=64)),
                ('ownership', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('date', models.DateField()),
                ('auth_name', models.CharField(max_length=64)),
                ('auth_desig', models.CharField(max_length=64)),
                ('auth_mob', models.CharField(max_length=64)),
                ('beds_icu', models.IntegerField(blank=True, default=0, null=True)),
                ('beds_others', models.IntegerField(blank=True, default=0, null=True)),
                ('beds_ot', models.IntegerField(blank=True, default=0, null=True)),
                ('beds_total', models.IntegerField(blank=True, default=0, null=True)),
                ('address', models.CharField(max_length=128)),
                ('bio_auth1_name', models.CharField(max_length=64)),
                ('bio_auth1_mob', models.CharField(default=0, max_length=64)),
                ('bio_auth2_name', models.CharField(max_length=64)),
                ('bio_auth2_mob', models.CharField(default=0, max_length=64)),
                ('supervisor_name', models.CharField(max_length=64)),
                ('supervisor_mob', models.CharField(default=0, max_length=64)),
                ('supervisor_name2', models.CharField(max_length=64)),
                ('supervisor_mob2', models.CharField(default=0, max_length=64)),
                ('status', models.CharField(max_length=64)),
                ('key', models.CharField(max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SignUp', verbose_name='Email ID')),
            ],
        ),
        migrations.CreateModel(
            name='Waste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('hospital_code', models.CharField(max_length=64)),
                ('key', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('waste1', models.IntegerField(blank=True, default=0, null=True)),
                ('waste2', models.IntegerField(blank=True, default=0, null=True)),
                ('waste3', models.IntegerField(blank=True, default=0, null=True)),
                ('waste4', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]
