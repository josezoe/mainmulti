from django import forms
from django.utils import timezone
from .models import Event, EventCategory, EventRating, EventComment, Booking
from django.apps import apps
from django.forms import modelform_factory
from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import EventSerializer
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render  


class EventForm(forms.ModelForm):
    categories = forms.CharField(required=False, help_text="Enter a comma-separated list of categories", widget=forms.Textarea)
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'date', 'location', 'country',
            'base_price', 'discount_percentage', 'early_bird_discount',
            'categories', 'is_active', 'event_image', 'datetime_from',
            'datetime_to', 'bulk_discount_threshold', 'bulk_discount_percentage'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'datetime_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'datetime_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now():
            raise forms.ValidationError("The event date cannot be in the past.")
        return date

    def clean_datetime_from(self):
        datetime_from = self.cleaned_data.get('datetime_from')
        if datetime_from < timezone.now():
            raise forms.ValidationError("The start time cannot be in the past.")
        return datetime_from

    def clean_datetime_to(self):
        datetime_to = self.cleaned_data.get('datetime_to')
        datetime_from = self.cleaned_data.get('datetime_from')
        if datetime_to and datetime_from and datetime_to <= datetime_from:
            raise forms.ValidationError("The end time must be after the start time.")
        return datetime_to
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Country = apps.get_model('users', 'Country')
        self.fields['country'].queryset = Country.objects.all()


class EventCategoryForm(forms.ModelForm):
    class Meta:
        model = EventCategory
        fields = ['name']

class EventRatingForm(forms.ModelForm):
    class Meta:
        model = EventRating
        fields = ['rating']

    def __init__(self, *args, **kwargs):
        super(EventRatingForm, self).__init__(*args, **kwargs)
        self.fields['rating'].widget = forms.RadioSelect(choices=[(i, i) for i in range(1, 6)])

class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['comment']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_people']
        widgets = {
            'number_of_people': forms.NumberInput(attrs={'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        if event:
            self.fields['number_of_people'].help_text = f"Price per person: {event.base_price}"

    def clean_number_of_people(self):
        number_of_people = self.cleaned_data.get('number_of_people')
        if number_of_people < 1:
            raise forms.ValidationError("Number of attendees must be at least 1.")
        return number_of_people
    
@login_required
def rate_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        form = EventRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.event = event
            rating.user = request.user
            rating.save()
            messages.success(request, 'Your rating has been submitted.')
            return redirect('events:event_detail', slug=slug)
    else:
        form = EventRatingForm()
    return render(request, 'events/rate_event.html', {'form': form, 'event': event})

@login_required
def comment_on_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        form = EventCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.user = request.user
            # Assuming you have a way to link the user's booking
            booking = Booking.objects.filter(event=event, user=request.user).first()
            if not booking:
                messages.error(request, "You must have a booking to comment on this event.")
                return redirect('events:event_detail', slug=slug)
            comment.booking = booking
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('events:event_detail', slug=slug)
    else:
        form = EventCommentForm()
    return render(request, 'events/comment_event.html', {'form': form, 'event': event})