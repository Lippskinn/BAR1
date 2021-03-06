# Generated by Django 2.0.5 on 2018-05-17 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Name des Ansprechpartners/in')),
                ('mail', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=32, verbose_name='Telefonnummer')),
                ('mobile', models.CharField(blank=True, max_length=32, verbose_name='Handynummer')),
                ('fax', models.CharField(blank=True, max_length=32, verbose_name='Fax Nummer')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(verbose_name='Beschreibung')),
                ('isGift', models.BooleanField()),
                ('image', models.ImageField(blank=True, upload_to='imgs/items/', verbose_name='Bild')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('categories', models.ManyToManyField(to='ressourcenpool.Category', verbose_name='Kategorien')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ressourcenpool.Contact')),
            ],
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Lender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation', models.CharField(blank=True, max_length=128)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ressourcenpool.Contact')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ressourcenpool.ItemType', verbose_name='Typ'),
        ),
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ressourcenpool.Lender'),
        ),
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ressourcenpool.ItemType'),
        ),
    ]
