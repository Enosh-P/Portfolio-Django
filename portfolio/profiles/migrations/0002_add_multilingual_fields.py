# Generated manually for multilingual support

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        # Add new language-specific fields
        migrations.AddField(
            model_name='profile',
            name='title_en',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='title_de',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='title_ta',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='hero_statement_en',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='hero_statement_de',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='hero_statement_ta',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='description_en',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='description_de',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='description_ta',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='linkedin_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='github_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='cv_file',
            field=models.FileField(blank=True, null=True, upload_to='cv/'),
        ),
        # Data migration will be in next migration
    ]

