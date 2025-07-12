from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    store_id = models.IntegerField()
    current_stock = models.PositiveIntegerField()
    weekly_sales_rate = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_dead_stock = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.brand})"
    




# models.py
from django.db import models

class Notification(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title


    @classmethod
    def create_dead_stock_alert(cls, product):
        cls.objects.create(
            product=product,
            title=f"Dead Stock Alert: {product.name}",
            message=(
                f"Product '{product.name}' at Store {product.store_id} has been marked as dead stock. "
                f"Stock: {product.current_stock}, Sales Rate: {product.weekly_sales_rate}"
            )
        )

class TransferRequest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    from_store_id = models.IntegerField()
    to_store_id = models.IntegerField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer of {self.quantity} x {self.product.name} from Store {self.from_store_id} to Store {self.to_store_id}"

