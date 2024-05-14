from rest_framework import serializers
from .models import *

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields='__all__'
class RazorpaySerializer(serializers.ModelSerializer):
    class Meta:
        model=RazorpayCreateOrder
        fields='__all__'



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['razorpay_payment_id', 'razorpay_order_id', 'razorpay_signature', 'amount', 'currency', 'status', 'created_at']        