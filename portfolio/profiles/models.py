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
    TOP_BAR_SHARED_FIELDS = (
        'linkedin_url',
        'github_url',
        'cv_file',
        'cv_file_en',
        'cv_file_de',
        'cv_file_ta',
    )

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

    # Language-specific cv
    cv_file_en = models.FileField(upload_to='cv/', blank=True, null=True, default='cv/Enosh_CV.pdf')
    cv_file_de = models.FileField(upload_to='cv/', blank=True, null=True, default='cv/Enosh_lebenslauf.pdf')
    cv_file_ta = models.FileField(upload_to='cv/', blank=True, null=True, default='cv/Enosh_CV.pdf')
    
    hero_statement_en = models.CharField(max_length=255, blank=True, help_text="A short tagline or statement (e.g., 'Passionate developer building amazing things')")
    hero_statement_de = models.CharField(max_length=255, blank=True)
    hero_statement_ta = models.CharField(max_length=255, blank=True)
    
    description_en = models.TextField()
    description_de = models.TextField(blank=True)
    description_ta = models.TextField(blank=True)
    
    # Category mapping
    categories = models.ManyToManyField('Category', blank=True, related_name='profiles',
                                       help_text="Select which categories this profile should be displayed for")

    def save(self, *args, **kwargs):
        """
        Keep top-bar fields shared across all profiles.
        Updating one profile syncs social links/CV files to the rest.
        """
        shared_values_before = None
        if self.pk:
            shared_values_before = Profile.objects.filter(pk=self.pk).values(
                *self.TOP_BAR_SHARED_FIELDS
            ).first()

        super().save(*args, **kwargs)

        shared_values_after = {
            field: getattr(self, field).name if hasattr(getattr(self, field), 'name') else getattr(self, field)
            for field in self.TOP_BAR_SHARED_FIELDS
        }

        if shared_values_before is not None:
            shared_values_before = {
                key: (value or '')
                for key, value in shared_values_before.items()
            }
            normalized_after = {
                key: (value or '')
                for key, value in shared_values_after.items()
            }
            if shared_values_before == normalized_after:
                return

        Profile.objects.exclude(pk=self.pk).update(**shared_values_after)

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
    
    def get_cv(self, language='en'):
        """Get description in specified language"""
        field_name = f'cv_file_{language}'
        cv_file = getattr(self, field_name, None)
        if language == 'de':
            self.cv_file_de = "cv/Enosh_lebenslauf.pdf"
            return self.cv_file_de
        if language == 'en':
            self.cv_file_en = "cv/Enosh_CV.pdf"
            return self.cv_file_en
        if language == 'ta':
            self.cv_file_ta = "cv/Enosh_CV.pdf"
            return self.cv_file_ta
        return cv_file or self.cv_file_en


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
