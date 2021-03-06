# Generated by Django 2.0.5 on 2018-05-20 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ressourcenpool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ressourcenpool.ItemType', verbose_name='Typ'),
        ),
        migrations.AlterField(
            model_name='item',
            name='isGift',
            field=models.BooleanField(verbose_name='Als Geschenk anbieten?'),
        ),
        migrations.AlterField(
            model_name='lender',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ressourcenpool.Contact', verbose_name='Kontaktdaten'),
        ),
        migrations.AlterField(
            model_name='lender',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Name'),
        ),
    ]
