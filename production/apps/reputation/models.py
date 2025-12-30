from django.db import models

class Platform(models.Model):
    PLATFORM_CHOICES = (
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('google', 'Google Reviews'),
        ('twitter', 'Twitter'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    icon = models.ImageField(upload_to='platforms/', blank=True, null=True)
    
    def __str__(self):
        return self.get_name_display()

class Review(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='reviews')
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text="Rating out of 5")
    review_url = models.URLField(blank=True, null=True)
    review_date = models.DateField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author_name} on {self.platform}"
