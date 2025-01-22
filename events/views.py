from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Event, EventCategory, EventRating, EventComment, Booking, Ticket  # Added Ticket model
from .serializers import EventSerializer
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import EventForm, EventCategoryForm, EventRatingForm, EventCommentForm, BookingForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render  

# Class-based view for creating events via traditional Django views
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')

    def form_valid(self, form):
        form.instance.vendor = self.request.user
        return super().form_valid(form)

# Class-based view for listing event categories
class EventCategoryListView(ListView):
    model = EventCategory
    template_name = 'events/event_category_list.html'
    context_object_name = 'categories'

# Class-based view for creating event categories
class EventCategoryCreateView(CreateView):
    model = EventCategory
    form_class = EventCategoryForm
    template_name = 'events/event_category_form.html'
    success_url = reverse_lazy('events:event_category_list')

# Class-based view for updating event categories
class EventCategoryUpdateView(UpdateView):
    model = EventCategory
    form_class = EventCategoryForm
    template_name = 'events/event_category_form.html'
    success_url = reverse_lazy('events:event_category_list')

# Class-based view for deleting event categories
class EventCategoryDeleteView(DeleteView):
    model = EventCategory
    template_name = 'events/event_category_confirm_delete.html'
    success_url = reverse_lazy('events:event_category_list')

# Class-based view for listing events via traditional Django views
class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 10  # Example pagination

# Class-based view for showing event details
class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.vendor != self.request.user:
            raise PermissionError("You do not have permission to view this event.")
        return obj

# Class-based view for updating events
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.vendor != self.request.user:
            raise PermissionError("You do not have permission to edit this event.")
        return obj


# Class-based view for deleting events
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:event_list')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.vendor != self.request.user:
            raise PermissionError("You do not have permission to delete this event.")

# Class-based view for creating bookings
class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'events/booking_form.html'  # Adjust this to your template path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

class BookingDetailView(DetailView):
    model = Booking
    template_name = 'events/booking_detail.html'  # Adjust this to your template path
    context_object_name = 'booking'

# Function view for rating events
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

# Function view for commenting on events
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

# Function view for canceling bookings
@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        # Here you would implement the cancellation logic
        booking.delete()
        messages.success(request, 'Your booking has been canceled.')
        return redirect('events:event_list')
    return render(request, 'events/confirm_cancel_booking.html', {'booking': booking})

# Function view for event analytics
@login_required
def event_analytics(request, slug):
    event = get_object_or_404(Event, slug=slug)
    # Implement analytics logic here
    context = {
        'event': event,
        # Add analytics data to context
    }
    return render(request, 'events/event_analytics.html', context)

# Function view for creating payment
@login_required
def create_payment(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if request.method == 'POST':
        # Payment processing logic here
        messages.success(request, 'Payment was processed successfully.')
        return redirect('events:confirm_payment', booking_id=booking_id)
    return render(request, 'events/create_payment.html', {'booking': booking})

# Function view for confirming payment
@login_required
def confirm_payment(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    # Payment confirmation logic
    context = {'booking': booking}
    return render(request, 'events/confirm_payment.html', context)

# Function view for viewing ticket
@login_required
def view_ticket(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    # Logic to display or process ticket details
    return render(request, 'events/view_ticket.html', {'booking': booking, 'ticket': booking.ticket})

# Function view for redeeming ticket
@login_required
def redeem_ticket(request):
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        try:
            booking = Booking.objects.get(id=ticket_id, user=request.user)
            if booking.ticket.redeem():
                messages.success(request, 'Ticket redeemed successfully.')
            else:
                messages.error(request, 'Ticket already redeemed.')
        except Booking.DoesNotExist:
            messages.error(request, 'Invalid ticket ID.')
    return render(request, 'events/redeem_ticket.html')

@login_required
def scan_barcode(request):
    if request.method == 'POST':
        barcode_data = request.POST.get('barcode_data')
        result, message = Ticket.scan_barcode(barcode_data)
        if result:
            messages.success(request, message)
        else:
            messages.error(request, message)
    return render(request, 'events/scan_barcode.html')

# API view for listing and creating events
class EventListAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# API view for retrieving, updating, or deleting an event
class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Custom view for obtaining and returning authentication token
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
