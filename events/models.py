from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from taggit.managers import TaggableManager
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw

class EventCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    country = models.ForeignKey('users.Country', on_delete=models.CASCADE)
    vendor = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'user_type': 'vendor'})
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Discount based on number of people
    early_bird_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Discount for early booking
    categories = TaggableManager(help_text="A comma-separated list of categories for this event", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    slug = models.SlugField(unique=True, default=uuid.uuid4) 
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    event_image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    
    # Event Duration
    duration = models.DurationField(null=True, blank=True, help_text="Duration of the event")
    datetime_from = models.DateTimeField(null=True, blank=True)
    datetime_to = models.DateTimeField(null=True, blank=True)

    # Bulk Discount
    bulk_discount_threshold = models.PositiveIntegerField(default=10, help_text="Number of attendees needed for bulk discount")
    bulk_discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Discount percentage for bulk booking")

    # Rating
    average_rating = models.FloatField(default=0.0)
    rating_count = models.PositiveIntegerField(default=0)

    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/event/{self.slug}/"
    
    def get_update_url(self):
        return f"/event/{self.slug}/update/"
    
    def get_delete_url(self):
        return f"/event/{self.slug}/delete/"
    
    def calculate_total_price(self, number_of_people):
        total = self.base_price * number_of_people
        
        # Apply early bird discount
        if self.date > timezone.now() + timezone.timedelta(days=30):
            total *= (1 - self.early_bird_discount / 100)
        
        # Apply bulk discount
        if number_of_people >= self.bulk_discount_threshold:
            total *= (1 - self.bulk_discount_percentage / 100)

        # Apply standard discount percentage (if any)
        total *= (1 - self.discount_percentage / 100)

        return max(0, total)

    def set_duration(self):
        if self.datetime_from and self.datetime_to:
            self.duration = self.datetime_to - self.datetime_from
            self.save()

    def save(self, *args, **kwargs):
        if self.datetime_from and self.datetime_to and not self.duration:
            self.set_duration()
        super().save(*args, **kwargs)
        self.update_unique_id()

    def update_unique_id(self):
        if not hasattr(self, 'unique_id') or not self.unique_id:
            self.unique_id = f"{self.vendor.vendor_unique_id}-{uuid.uuid4()}"
            self.save(update_fields=['unique_id'])

    def update_average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            avg = ratings.aggregate(models.Avg('rating'))['rating__avg']
            self.average_rating = round(avg, 2)
            self.rating_count = ratings.count()
        else:
            self.average_rating = 0.0
            self.rating_count = 0
        self.save()

    def sentiment_analysis(self):
        from textblob import TextBlob
        comments = self.comments.all()
        positive = negative = neutral = 0
        for comment in comments:
            analysis = TextBlob(comment.comment)
            if analysis.sentiment.polarity > 0:
                positive += 1
            elif analysis.sentiment.polarity < 0:
                negative += 1
            else:
                neutral += 1
        total = positive + negative + neutral
        return {
            'positive': round((positive / total) * 100, 2) if total else 0,
            'negative': round((negative / total) * 100, 2) if total else 0,
            'neutral': round((neutral / total) * 100, 2) if total else 0,
        } if total else {'positive': 0, 'negative': 0, 'neutral': 0}

    def common_words(self, count=10):
        from collections import Counter
        words = []
        for comment in self.comments.all():
            words.extend([word.lower() for word in comment.comment.split() if word.isalnum()])
        return Counter(words).most_common(count)
    

class Booking(models.Model):
    # ... existing fields ...
    redeemed = models.BooleanField(default=False)
    number_of_people = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'ticket') or not self.ticket:
            self.create_ticket()

    def create_ticket(self):
        if not hasattr(self, 'ticket') or not self.ticket:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f"Event ID: {self.event.unique_id}, Booking ID: {self.id}")
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            ticket = Ticket.objects.create(
                booking=self,
                qr_code=ContentFile(img_byte_arr, name=f"ticket_{self.id}.png")
            )

class EventRating(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.event.update_average_rating()

class EventComment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user', 'booking')



class Ticket(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='ticket')
    qr_code = models.ImageField(upload_to="tickets/")

    def __str__(self):
        return f"Ticket for {self.booking.user.username} - Event: {self.booking.event.title}"

    def redeem(self):
        if not self.booking.redeemed:
            self.booking.redeemed = True
            self.booking.save()
            return True
        return False

    @staticmethod
    def scan_barcode(barcode_data):
        # This method would be used to scan QR codes. Here's a placeholder:
        import re
        match = re.search(r'Event ID: (.+?), Booking ID: (\d+)', barcode_data)
        if match:
            event_id, booking_id = match.groups()
            try:
                booking = Booking.objects.get(event__unique_id=event_id, id=booking_id)
                if booking.ticket.redeem():
                    return booking, "Ticket redeemed successfully"
                else:
                    return booking, "Ticket already redeemed"
            except Booking.DoesNotExist:
                return None, "Invalid or non-existent ticket"
        return None, "Invalid QR code format"
