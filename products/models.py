from django.db import models
from django.db.models import Q


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    slug = models.SlugField(unique=True, verbose_name="شناسه دسته‌بندی")

    class Meta:
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="دسته‌بندی")
    name = models.CharField(max_length=255, verbose_name="نام محصول")
    price = models.PositiveBigIntegerField(verbose_name="قیمت محصول")
    stock = models.PositiveIntegerField(default=0, verbose_name="تعداد موجود در انبار")
    discount_price = models.PositiveBigIntegerField(null=True, blank=True, verbose_name="قیمت با تخفیف")
    slug = models.SlugField(unique=True, verbose_name="شناسه محصول")
    description = models.TextField(verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="فعال بودن محصول")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to="products/", verbose_name="تصویر محصول")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="محصول")
    is_primary = models.BooleanField(default=False, verbose_name="تصویر اصلی")

    class Meta:
        verbose_name = "عکس محصول"
        verbose_name_plural = "عکس‌های محصولات"
        ordering = ["-is_primary", "id"]
        
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                condition=Q(is_primary=True),
                name="unique_primary_image_per_product"
            )
        ]

    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(
                product_id=self.product_id,
                is_primary=True 
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - تصویر {self.pk}"