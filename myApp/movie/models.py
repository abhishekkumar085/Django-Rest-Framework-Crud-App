from django.db import models

# Create your models here.
class Movie(models.Model):
    name=models.CharField(max_length=100)
    director=models.TextField()
    completed=models.BooleanField(default=True)


    def __str__(self):
        return self.name
    


class RazorpayCreateOrder(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    currency = models.CharField(max_length=10, default="INR")
    order_id=models.CharField(max_length=255,default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)
    
class Payment(models.Model):
    razorpay_payment_id = models.CharField(max_length=100, unique=True)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_signature = models.CharField(max_length=100)  # Add this field for the signature
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.razorpay_payment_id)