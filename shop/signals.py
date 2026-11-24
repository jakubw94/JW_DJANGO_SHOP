from django.dispatch import receiver
from .models import Product
from django.db.models.signals import post_delete
import os
import shutil
from django.conf import settings


# Deleting folders with images after every product delete #
@receiver(post_delete, sender=Product)
def delete_product_images(sender, instance, **kwargs):
    try:
        product_images_path = os.path.join(settings.MEDIA_ROOT, "product_images", str(instance.id))
        if os.path.exists(product_images_path):
            shutil.rmtree(product_images_path)
    except Exception:
        ...