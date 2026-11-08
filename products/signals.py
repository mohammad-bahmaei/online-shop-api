from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, ProductImage

@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
@receiver(post_save, sender=ProductImage)
@receiver(post_delete, sender=ProductImage)
def clear_product_cache(sender, instance, **kwargs):
    cache.delete("product_list")

    if sender == Product:
        slug = instance.slug
    
    else:

        slug = Product.objects.filter(pk=instance.product_id).values_list("slug", flat=True).first()

    if slug:
        cache.delete(f"product_{slug}")
