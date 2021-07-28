from django.db import models

from django.contrib.auth.models import User
from django.forms import ModelForm


from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Category(models.Model):
    STATUS=(
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
        STATUS =(
            ('True', 'True'),
            ('True', 'True'),
        )

        AVAILABLE =(
            ('In Stock', 'In Stock'),
            ('Out of Stock', 'Out of Stock'),
            ('Restocked', 'Restocked'),
        )

        category = models.ForeignKey(Category, on_delete=models.CASCADE )
        title = models.CharField(max_length=150, blank=True)
        keywords = models.CharField(max_length=255)
        description = models.CharField(max_length=255)
        image = models.ImageField(blank=True, upload_to='images/')
        price = models.FloatField(null=True, blank=True)
        sizes = models.CharField(max_length=30, null=True, default='Large')
        color = models.CharField(max_length=30, null=True, default='Black')
        discount_price= models.FloatField(blank=True, null=True)
        available = models.CharField(max_length=15, choices=AVAILABLE, default='In Stock')
        quantity_instock = models.IntegerField(null=True, blank=True, default=1000)
        minquantity = models.IntegerField(blank=True)
        amount = models.IntegerField(blank=True, null=True)
        status = models.CharField(max_length=10, choices=STATUS)
        slug = models.SlugField(null=True, unique=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now_add=True)
        featured = models.BooleanField(blank=True)
        new_prod = models.BooleanField(blank=True)
        new_prod_slide = models.BooleanField(blank=True, default=1)
        new_prod_slidea = models.BooleanField(blank=True, default=1)
        popular = models.BooleanField(blank=True)
        upcoming = models.BooleanField(blank=True)
        bestselling = models.BooleanField(blank=True)
        details = RichTextUploadingField()

        def __str__(self):
            return self.title

        def image_tag(self):
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

        image_tag.short_description = 'image'

        def get_absolute_url(self):
            return reverse("category_detail", kwargs={"slug": self.slug})


class Images(models.Model):
            product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, blank=True)
            image = models.ImageField(blank=True, upload_to='images/')






class Carousel_a(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__ (self):
        return self.title

class Carousel_b(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__ (self):
        return self.title


class Carousel_c(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__ (self):
        return self.title

class Carousel_d(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__ (self):
        return self.title

