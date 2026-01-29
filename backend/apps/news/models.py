from django.db import models


class Category(models.Model):
    # This categories is used by following the newsapi docs categories.
    CATEGORY_CHOICES = [
        ('business', 'Business'),
        ('entertainment', 'Entertainment'),
        ('general', 'General'),
        ('health', 'Health'),
        ('science', 'Science'),
        ('sports', 'Sports'),
        ('technology', 'Technology'),
    ]
    
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.get_name_display()


class Language(models.Model):

    # For simplicity, only a few languages are included (there are more supported by NewsAPI).
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fr', 'French'),
        ('ar', 'Arabic'),
    ]
    code = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, unique=True)

    def __str__(self):
        return self.get_code_display()



class Country(models.Model):

    # For simplicity, only a few countries are included (there are more supported by NewsAPI).
    COUNTRY_CHOICES = [
        ('us', 'United States'),
        ('fr', 'France'),
        ('eg', 'Egypt'),
        ('ca', 'Canada'),
    ]
    
    code = models.CharField(max_length=2, choices=COUNTRY_CHOICES, unique=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.get_code_display()



class Source(models.Model):
    """
    Represents a news source from NewsAPI.
    A source has its own category, language, and country.
    """
    source_id = models.CharField(max_length=100, unique=True)  # e.g., "bbc-news"
    name = models.CharField(max_length=100)  # e.g., "BBC News"
    description = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=2000,null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name='sources')
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sources'
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sources'
    )

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    """
    Represents a news article.
    Denormalized fields (category, language, country) are stored for faster filtering.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)
    content = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField()
    
    # Relationship to source (normalized)
    source = models.ForeignKey(
        Source,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )
    
    # Denormalized fields for faster filtering (copied from source)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['language']),
            models.Index(fields=['country']),
            models.Index(fields=['published_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-populate denormalized fields from source
        if self.source:
            self.category = self.source.category
            self.language = self.source.language
            self.country = self.source.country
        super().save(*args, **kwargs)