# Generated manually - add AboutMe model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_migrate_data_and_remove_old_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutMe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('en', 'English'), ('de', 'Deutsch'), ('ta', 'தமிழ்')], default='en', max_length=2)),
                ('content', models.TextField()),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'About Me',
                'ordering': ['language', 'order'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='aboutme',
            unique_together={('language', 'order')},
        ),
    ]


