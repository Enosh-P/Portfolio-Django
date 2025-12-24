from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Category

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'slug', 'has_picture', 'has_social_links']
    list_display_links = ['title_en']
    search_fields = ['slug', 'title_en', 'title_de', 'title_ta', 'hero_statement_en', 'description_en']
    readonly_fields = ['preview_picture']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('slug',),
            'description': 'Unique identifier for your profile (e.g., "main-profile")'
        }),
        ('Profile Picture', {
            'fields': ('profile_picture', 'preview_picture'),
            'description': 'Your profile picture will appear on the right side of the About Me section'
        }),
        ('English Content (Primary)', {
            'fields': ('title_en', 'hero_statement_en', 'description_en'),
            'description': 'Title and Description are required. Hero Statement is optional - a short tagline that appears in bold below your title.'
        }),
        ('Social Links & Files', {
            'fields': ('linkedin_url', 'github_url', 'cv_file'),
            'description': 'These appear in the top bar of your portfolio'
        }),
        ('German Translation (Optional)', {
            'fields': ('title_de', 'hero_statement_de', 'description_de'),
            'classes': ('collapse',),
            'description': 'German translations. If not provided, English will be used.'
        }),
        ('Tamil Translation (Optional)', {
            'fields': ('title_ta', 'hero_statement_ta', 'description_ta'),
            'classes': ('collapse',),
            'description': 'Tamil translations. If not provided, English will be used.'
        }),
        ('Category Mapping', {
            'fields': ('categories',),
            'description': 'Select which categories this profile should be displayed for. If no categories are selected, this profile will be used as the default for all categories.'
        }),
    )
    filter_horizontal = ['categories']
    
    def has_picture(self, obj):
        """Check if profile has a picture"""
        return bool(obj.profile_picture)
    has_picture.short_description = 'Has Picture'
    has_picture.boolean = True
    
    def has_social_links(self, obj):
        """Check if profile has social links"""
        links = []
        if obj.linkedin_url:
            links.append('LinkedIn')
        if obj.github_url:
            links.append('GitHub')
        if obj.cv_file:
            links.append('CV')
        return ', '.join(links) if links else 'None'
    has_social_links.short_description = 'Social Links'
    
    def preview_picture(self, obj):
        """Show preview of profile picture"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; border: 2px solid #4a4a6a;" />',
                obj.profile_picture.url
            )
        return 'No picture uploaded'
    preview_picture.short_description = 'Preview'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'slug', 'category_type', 'order', 'has_skills', 'mapped_profiles_count']
    list_editable = ['order']
    list_filter = ['category_type']
    search_fields = ['slug', 'name_en', 'name_de', 'name_ta', 'skills']
    fieldsets = (
        ('Basic Information', {
            'fields': ('slug', 'category_type', 'icon', 'order')
        }),
        ('Names', {
            'fields': ('name_en', 'name_de', 'name_ta')
        }),
        ('Console Skills', {
            'fields': ('skills',),
            'description': 'Enter skills text to display in the console when this category is selected. Use bullet points (•) or plain text. Each line will be displayed in the console.'
        }),
    )
    
    def has_skills(self, obj):
        """Check if category has skills text"""
        return bool(obj.skills and obj.skills.strip())
    has_skills.short_description = 'Has Skills'
    has_skills.boolean = True
    
    def mapped_profiles_count(self, obj):
        """Count of profiles mapped to this category"""
        return obj.profiles.count()
    mapped_profiles_count.short_description = 'Mapped Profiles'
