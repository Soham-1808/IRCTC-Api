# railway/views.py
from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .models import Train, Booking
from .serializers import UserRegistrationSerializer, TrainSerializer, BookingSerializer

# 1. Register a User
class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. Login User
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Helper function to check Admin API key
def check_admin_api_key(request):
    api_key = request.headers.get('X-API-KEY')
    return api_key == settings.ADMIN_API_KEY

# 3. Add a New Train (Admin Only)
class AddTrainView(APIView):
    def post(self, request):
        if not check_admin_api_key(request):
            return Response({'error': 'Unauthorized. Invalid API Key.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = TrainSerializer(data=request.data)
        if serializer.is_valid():
            train = serializer.save()
            return Response(TrainSerializer(train).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 4. Get Seat Availability
# Expects query parameters: ?source=...&destination=...
class SeatAvailabilityView(APIView):
    def get(self, request):
        source = request.query_params.get('source')
        destination = request.query_params.get('destination')
        if not source or not destination:
            return Response({'error': 'Source and destination are required.'}, status=status.HTTP_400_BAD_REQUEST)
        trains = Train.objects.filter(source__iexact=source, destination__iexact=destination)
        serializer = TrainSerializer(trains, many=True)
        return Response(serializer.data)

# 5. Book a Seat (Requires authentication)
class BookSeatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        train_id = request.data.get('train_id')
        if not train_id:
            return Response({'error': 'Train ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                # Lock the train row to avoid race conditions
                train = Train.objects.select_for_update().get(id=train_id)
                if train.available_seats > 0:
                    # Decrement available seats
                    train.available_seats = F('available_seats') - 1
                    train.save()
                    # Refresh from DB to get the updated value
                    train.refresh_from_db()
                    # Create a booking record
                    booking = Booking.objects.create(user=request.user, train=train)
                    serializer = BookingSerializer(booking)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'No seats available on this train.'}, status=status.HTTP_400_BAD_REQUEST)
        except Train.DoesNotExist:
            return Response({'error': 'Train not found.'}, status=status.HTTP_404_NOT_FOUND)

# 6. Get Specific Booking Details (Requires authentication)
class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            serializer = BookingSerializer(booking)
            return Response(serializer.data)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)
