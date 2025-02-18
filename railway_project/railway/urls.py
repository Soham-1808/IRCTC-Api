# railway/urls.py
from django.urls import path
from .views import (
    RegisterView, LoginView, AddTrainView,
    SeatAvailabilityView, BookSeatView, BookingDetailView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('train/', AddTrainView.as_view(), name='add_train'),  # admin endpoint
    path('trains/', SeatAvailabilityView.as_view(), name='seat_availability'),
    path('book/', BookSeatView.as_view(), name='book_seat'),
    path('booking/<int:booking_id>/', BookingDetailView.as_view(), name='booking_detail'),
]
