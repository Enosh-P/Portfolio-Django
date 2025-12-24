from django.contrib import admin
from .models import SkillCategory, Skill

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name_en', 'name_de', 'name_ta', 'order']
    list_editable = ['order']
    search_fields = ['slug', 'name_en', 'name_de', 'name_ta']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'category', 'order']
    list_filter = ['category']
    list_editable = ['order']
    search_fields = ['name_en', 'name_de', 'name_ta', 'description_en']
    fieldsets = (
        ('Basic Info', {
            'fields': ('category', 'order')
        }),
        ('English', {
            'fields': ('name_en', 'description_en')
        }),
        ('German', {
            'fields': ('name_de', 'description_de'),
            'classes': ('collapse',)
        }),
        ('Tamil', {
            'fields': ('name_ta', 'description_ta'),
            'classes': ('collapse',)
        }),
    )
