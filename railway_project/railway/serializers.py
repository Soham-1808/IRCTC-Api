# railway/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Train, Booking

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    train = TrainSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'train', 'booking_time']
        read_only_fields = ['id', 'user', 'train', 'booking_time']
