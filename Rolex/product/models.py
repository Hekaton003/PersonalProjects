from PIL import Image
from django.db import models


# Create your models here.

class Watch(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    image = models.ImageField(upload_to="images")
    price = models.DecimalField(max_digits=20,decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path,"PNG")

