from rest_framework import serializers
from .models import CustomUser, Vendor, Country, State, City, Timezone

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class TimezoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timezone
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    state = StateSerializer(read_only=True)
    city = CitySerializer(read_only=True)
    preferred_timezone = TimezoneSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'user_type',
             'unique_id', 'phone', 'country', 'state', 'city', 'profile_image',
            'preferred_currency', 'preferred_timezone', 'age', 'gender',
            'income_level', 'housing_status', 'postal_code',
            'geolocation', 'last_page_visited', 'visit_count', 'last_visit',
            'search_history', 'purchase_history', 'last_purchase_date',
            'purchase_count', 'total_spent', 'segment', 'lifestyle',
            'interests', 'marketing_preferences', 'behavior_tags',
            'date_joined'
        ]

class VendorSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    state = StateSerializer(read_only=True)
    city = CitySerializer(read_only=True)
    preferred_timezone = TimezoneSerializer(read_only=True)
    class Meta:
        model = Vendor
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'user_type', 'company_name', 'tax_id', 'slug', 'vendor_unique_id',
            'contact_person_name', 'phone_number', 'business_email', 'website',
            'address_line1', 'address_line2', 'direction', 'menu',
            'cuisine_type', 'cuisines', 'opening_hours', 'description',
            'about', 'facilities', 'atmosphere', 'spoken_languages',
            'payment_options', 'special_conditions', 'average_rating',
            'review_count', 'created_at', 'updated_at', 'is_vendor_superuser',
            'country', 'state', 'city', 'preferred_timezone', 'profile_image', 'is_active', 'phone',
            'date_joined', 'income_level', 'gender', 'housing_status', 'postal_code'
        ]