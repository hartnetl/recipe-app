from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager


# Recipe model

class Recipe(models.Model):
    STATUS = ((0, "Draft"), (1, "Published"))

    CATEGORY_CHOICE = (
        ("BFAST", "Breakfast"),
        ("LUNCH", "Lunch"),
        ("DINNER", "Dinner"),
        ("DRINKS", "Drinks"),
        ("OTHER", "Other"),
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="recipes")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    about = models.TextField()
    url = models.URLField(blank=True, max_length=200)
    nutrition = models.TextField(blank=True)
    servings = models.PositiveIntegerField()
    prep_time = models.CharField(max_length=20)
    cook_time = models.CharField(max_length=20)
    ingredients = models.TextField(null=True)
    method = models.TextField()
    tags = TaggableManager()
    status = models.IntegerField(choices=STATUS, default=0)
    featured_image = CloudinaryField('image', default='placeholder')
    approved = models.BooleanField(default=False)
    category = models.CharField(max_length=9, choices=CATEGORY_CHOICE,
                                default='OTHER')
    saved = models.ManyToManyField(User, related_name='saved_recipes',
                                   blank=True)

    # Using slugify found here https://kodnito.com/posts/slugify-urls-django/
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


# Comments model
class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='comments')

    name = models.CharField(max_length=40)
    email = models.EmailField()
    message = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_posted']

    def __str__(self):
        return f"Comment {self.message} by {self.name}"
