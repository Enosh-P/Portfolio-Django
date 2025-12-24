from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_de', 'title_ta', 'github_url']
    search_fields = ['title_en', 'title_de', 'title_ta', 'description_en']
    fieldsets = (
        ('Basic Info', {
            'fields': ('github_url', 'profiles')
        }),
        ('English', {
            'fields': ('title_en', 'description_en', 'tech_stack_en')
        }),
        ('German', {
            'fields': ('title_de', 'description_de', 'tech_stack_de'),
            'classes': ('collapse',)
        }),
        ('Tamil', {
            'fields': ('title_ta', 'description_ta', 'tech_stack_ta'),
            'classes': ('collapse',)
        }),
    )
    filter_horizontal = ['profiles']
