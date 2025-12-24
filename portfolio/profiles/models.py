from django.db import models

class Category(models.Model):
    """Categories that profiles can be mapped to"""
    CATEGORY_TYPES = [
        ('special', 'Special Category'),
        ('skill', 'Skill Category'),
    ]
    
    slug = models.SlugField(unique=True, max_length=50, help_text="Category identifier (e.g., 'about-me', 'cpp-developer')")
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES, default='special')
    
    # Skills text to display in console
    skills = models.TextField(blank=True, help_text="Skills text to display in console when this category is selected. Use bullet points or plain text.")
    
    # Language-specific names
    name_en = models.CharField(max_length=100)
    name_de = models.CharField(max_length=100, blank=True)
    name_ta = models.CharField(max_length=100, blank=True)
    
    icon = models.CharField(max_length=50, blank=True, help_text="Icon emoji or identifier")
    order = models.IntegerField(default=0, help_text="Display order in navigation")
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'slug']
    
    def __str__(self):
        return self.name_en
    
    def get_name(self, language='en'):
        """Get name in specified language"""
        field_name = f'name_{language}'
        name = getattr(self, field_name, None)
        return name or self.name_en

class Profile(models.Model):
    slug = models.SlugField(unique=True)
    
    # Social links and CV
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # Language-specific content
    title_en = models.CharField(max_length=100)
    title_de = models.CharField(max_length=100, blank=True)
    title_ta = models.CharField(max_length=100, blank=True)
    
    hero_statement_en = models.CharField(max_length=255, blank=True, help_text="A short tagline or statement (e.g., 'Passionate developer building amazing things')")
    hero_statement_de = models.CharField(max_length=255, blank=True)
    hero_statement_ta = models.CharField(max_length=255, blank=True)
    
    description_en = models.TextField()
    description_de = models.TextField(blank=True)
    description_ta = models.TextField(blank=True)
    
    # Category mapping
    categories = models.ManyToManyField('Category', blank=True, related_name='profiles',
                                       help_text="Select which categories this profile should be displayed for")

    def __str__(self):
        return self.title_en
    
    def get_title(self, language='en'):
        """Get title in specified language"""
        field_name = f'title_{language}'
        title = getattr(self, field_name, None)
        return title or self.title_en
    
    def get_hero_statement(self, language='en'):
        """Get hero statement in specified language"""
        field_name = f'hero_statement_{language}'
        statement = getattr(self, field_name, None)
        return statement or self.hero_statement_en
    
    def get_description(self, language='en'):
        """Get description in specified language"""
        field_name = f'description_{language}'
        desc = getattr(self, field_name, None)
        return desc or self.description_en


class AboutMe(models.Model):
    """About Me content for different languages"""
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('de', 'Deutsch'),
        ('ta', 'தமிழ்'),
    ]
    
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    content = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "About Me"
        ordering = ['language', 'order']
        unique_together = [['language', 'order']]
    
    def __str__(self):
        return f"About Me ({self.get_language_display()})"
