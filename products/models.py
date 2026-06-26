from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    category = models.CharField(max_length=100, db_index=True)
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.product_name
