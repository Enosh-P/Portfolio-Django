# Generated manually - Create initial categories

from django.db import migrations

def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('profiles', 'Category')
    SkillCategory = apps.get_model('skills', 'SkillCategory')
    
    # Create special categories
    categories_data = [
        {'slug': 'about-me', 'name_en': 'About Me', 'icon': '💾', 'order': 0, 'category_type': 'special'},
        {'slug': 'open-source', 'name_en': 'Open Sourced Projects', 'icon': '📦', 'order': 1, 'category_type': 'special'},
        {'slug': 'education', 'name_en': 'Education', 'icon': '🎓', 'order': 5, 'category_type': 'special'},
        {'slug': 'skills', 'name_en': 'Skills', 'icon': '🛠️', 'order': 6, 'category_type': 'special'},
    ]
    
    for cat_data in categories_data:
        Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name_en': cat_data['name_en'],
                'icon': cat_data['icon'],
                'order': cat_data['order'],
                'category_type': cat_data['category_type'],
            }
        )
    
    # Create categories linked to SkillCategories
    skill_categories = SkillCategory.objects.all()
    for skill_cat in skill_categories:
        Category.objects.get_or_create(
            slug=skill_cat.slug,
            defaults={
                'name_en': skill_cat.name_en,
                'name_de': skill_cat.name_de,
                'name_ta': skill_cat.name_ta,
                'icon': skill_cat.icon,
                'order': skill_cat.order + 2,  # After about-me and open-source
                'category_type': 'skill',
                'skill_category': skill_cat,
            }
        )

def reverse_create_categories(apps, schema_editor):
    Category = apps.get_model('profiles', 'Category')
    Category.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_add_category_mapping'),
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_categories, reverse_create_categories),
    ]

