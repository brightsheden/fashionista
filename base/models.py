from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db.utils import IntegrityError
from django.utils.text import slugify


# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(default=0.00, decimal_places=2,max_digits=10)
    thumbnail = models.ImageField(blank=True, null=True)
    afflink= models.URLField(blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    category =  models.CharField(default='fashion', max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=500,unique=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            # Handle the case where a slug conflict occurred
            base_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    def __str__(self):
        return self.product.name
    



class Blog(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)
    content = RichTextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title