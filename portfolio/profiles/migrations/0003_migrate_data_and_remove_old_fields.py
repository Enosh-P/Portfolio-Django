# Generated manually - migrate data and remove old fields

from django.db import migrations


def migrate_profile_data(apps, schema_editor):
    Profile = apps.get_model('profiles', 'Profile')
    for profile in Profile.objects.all():
        # Copy existing data to _en fields
        # Check if old fields exist (they will be removed in this migration)
        if hasattr(profile, 'title') and profile.title and not profile.title_en:
            profile.title_en = profile.title
        if hasattr(profile, 'hero_statement') and profile.hero_statement and not profile.hero_statement_en:
            profile.hero_statement_en = profile.hero_statement
        if hasattr(profile, 'description') and profile.description and not profile.description_en:
            profile.description_en = profile.description
        profile.save()


def reverse_migrate_profile_data(apps, schema_editor):
    # Reverse migration - copy _en fields back to old fields
    Profile = apps.get_model('profiles', 'Profile')
    for profile in Profile.objects.all():
        if hasattr(profile, 'title'):
            profile.title = profile.title_en
        if hasattr(profile, 'hero_statement'):
            profile.hero_statement = profile.hero_statement_en
        if hasattr(profile, 'description'):
            profile.description = profile.description_en
        profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_add_multilingual_fields'),
    ]

    operations = [
        migrations.RunPython(migrate_profile_data, reverse_migrate_profile_data),
        # Remove old fields
        migrations.RemoveField(
            model_name='profile',
            name='title',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='hero_statement',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='description',
        ),
    ]


