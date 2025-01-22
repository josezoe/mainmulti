from rest_framework import serializers
from .models import Event, EventCategory, EventRating, EventComment, Booking, Ticket
from django.contrib.auth import get_user_model

User = get_user_model()

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True, read_only=True)
    vendor = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date', 'location', 'country', 
            'vendor', 'base_price', 'discount_percentage', 'early_bird_discount', 
            'categories', 'is_active', 'created_at', 'updated_at', 'slug', 
            'is_approved', 'is_rejected', 'is_featured', 'event_image', 
            'datetime_from', 'datetime_to', 'bulk_discount_threshold', 
            'bulk_discount_percentage', 'average_rating', 'rating_count', 
            'unique_id'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'slug', 'average_rating', 'rating_count', 'unique_id']

    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        # If you want to set the unique_id when creating, do it here
        event.update_unique_id()
        return event

class EventRatingSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    
    class Meta:
        model = EventRating
        fields = ['id', 'event', 'user', 'rating', 'created_at']
        read_only_fields = ['id', 'created_at']

class EventCommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    
    class Meta:
        model = EventComment
        fields = ['id', 'event', 'user', 'booking', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    event = EventSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'event', 'user', 'booking_date', 'number_of_people', 'total_price', 'status', 'redeemed']
        read_only_fields = ['id', 'booking_date', 'total_price', 'redeemed']

class TicketSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'booking', 'qr_code']
        read_only_fields = ['id']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # If you want to show the QR code as a URL rather than the file path
        rep['qr_code'] = instance.qr_code.url if instance.qr_code else None
        return rep