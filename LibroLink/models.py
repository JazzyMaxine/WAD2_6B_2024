from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    website = models.URLField(blank=True) 
    picture = models.ImageField(upload_to='profile_images',blank=True) 
    
    def __str__(self): 
        return self.user.username
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book_name = models.CharField(max_length=255)
    book_author = models.CharField(max_length=255)
    review_text = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    book_image = models.ImageField(upload_to='book_images', blank=True, null=True)

    def __str__(self):
        return f"{self.book_name} by {self.book_author} - {self.user.username}"

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ['-rating'] 
        