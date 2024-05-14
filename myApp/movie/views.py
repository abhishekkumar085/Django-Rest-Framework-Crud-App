import uuid
from django.http import JsonResponse
from rest_framework import generics
from .models import *
from .serializers import MovieSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import razorpay

from django.conf import settings
from rest_framework.serializers import ValidationError
from rest_framework import status
from .serializers import PaymentSerializer



# create movies
class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Movie created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
# view details of movies
class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"message": "Movie retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
    # view all movies
class AllMoviesListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"message": "All movies retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
# update movies
class MovieUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    partial = True

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=self.partial)
        if serializer.is_valid():
            serializer.save()
            print("Movie updated successfully")  # Debugging
            return Response({"message": "Movie updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        print("Update error:", serializer.errors)  # Debugging
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
# for delete movies
class MovieDeleteView(generics.DestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({"message": "Movie deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# for Razorpay integration

         
            
            
            
            
# class RazopayCreateOrder(APIView):
#     def post(self, request, *args, **kwargs):
#         amount = request.data.get('amount')
#         currency = request.data.get('currency', 'INR')

#         # Create an Order instance
#         order = RazorpayCreateOrder(amount=amount, currency=currency)

#         # Initialize Razorpay client
#         client = razorpay.Client(auth=(
#             settings.RAZORPAY_KEY_ID,
#             settings.RAZORPAY_KEY_SECRET
#         ))

#         data = {
#             "amount": amount,
#             "currency": currency,
#         }

#         try:
#             # Create order on Razorpay
#             order_data = client.order.create(data=data)
#             # Save the order details to your database
#             order.order_id = order_data['id']
#             order.save()

#             return Response({"message": "Order created successfully", "order_data": order_data}, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             raise ValidationError(
#                 {
#                     "status_code": status.HTTP_400_BAD_REQUEST,
#                     "message": str(e),
#                 }
#             )            




class RazopayCreateOrder(APIView):
    def post(self, request, *args, **kwargs):
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'INR')

        # Initialize Razorpay client
        client = razorpay.Client(auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        ))

        data = {
            "amount": amount,
            "currency": currency,
        }

        try:
            # Create order on Razorpay
            order_data = client.order.create(data=data)
            # Save the order details to your database
            order = RazorpayCreateOrder.objects.create(
                amount=amount,
                currency=currency,
                order_id=order_data['id']  # Save Razorpay order ID in your database
            )

            return Response({"message": "Order created successfully", "order_data": order_data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": str(e),
                }
            )

# for payment verification

class PaymentVerification(APIView):
   
    def post(self, request, *args, **kwargs):
        data = request.data
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')

        client = razorpay.Client(auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        ))

        try:
            client.utility.verify_payment_signature({
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_signature': razorpay_signature
            })
            # Payment is verified
            payment = Payment.objects.create(
                razorpay_payment_id=razorpay_payment_id,
                razorpay_order_id=razorpay_order_id,
                razorpay_signature=razorpay_signature,
                amount=data.get('amount'),
                currency=data.get('currency'),
                status='SUCCESS'  # Set payment status
            )
            payment.save()

            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=200)
        except Exception as e:
            # Payment verification failed
            raise ValidationError(
                {
                    "status_code": 400,
                    "message": str(e),
                }
            )