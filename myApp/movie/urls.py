from django.urls import path
from .views import *
urlpatterns = [
    path('movies/', MovieListCreateView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/all/', AllMoviesListView.as_view(), name='all-movies-list'),  
    path('movies/delete/<int:pk>/', MovieDeleteView.as_view(), name='movie-delete'), 
    path('movies/update/<int:pk>/', MovieUpdateView.as_view(), name='movie-update'), 
    path('create_order/', RazopayCreateOrder.as_view(), name='create_order'),  # Razorpay URL
    path('verify_payment/', PaymentVerification.as_view(), name='verify_payment'),  # Payment verification URL
]