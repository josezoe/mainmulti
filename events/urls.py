from django.urls import path
from . import views
from .views import EventListView, EventListAPIView, EventDetailAPIView, CustomAuthToken, EventCategoryListView, EventCategoryCreateView, EventCategoryUpdateView, EventCategoryDeleteView, BookingCreateView, BookingDetailView

app_name = 'events'

urlpatterns = [
    # Event Management
    path('', views.EventListView.as_view(), name='event_list'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<slug:slug>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('<slug:slug>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    
    # Event Categories
    path('categories/', EventCategoryListView.as_view(), name='event_category_list'),
    path('categories/create/', EventCategoryCreateView.as_view(), name='event_category_create'),
    path('categories/<int:pk>/update/', EventCategoryUpdateView.as_view(), name='event_category_update'),
    path('categories/<int:pk>/delete/', EventCategoryDeleteView.as_view(), name='event_category_delete'),
    
    # Event Ratings and Comments
    path('<slug:slug>/rate/', views.rate_event, name='rate_event'),
    path('<slug:slug>/comment/', views.comment_on_event, name='comment_event'),
    
    # Booking
    path('<slug:slug>/book/', BookingCreateView.as_view(), name='book_event'),
    path('booking/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('booking/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),

    # Event Analytics
    path('<slug:slug>/analytics/', views.event_analytics, name='event_analytics'),
    
    # Payment and Confirmation
    path('payment/<int:booking_id>/', views.create_payment, name='create_payment'),
    path('confirm_payment/<int:booking_id>/', views.confirm_payment, name='confirm_payment'),
    
    # Ticket Management
    path('booking/<int:pk>/ticket/', views.view_ticket, name='view_ticket'),
    path('ticket/redeem/', views.redeem_ticket, name='redeem_ticket'),
    
    # QR Code Scanning
    path('ticket/scan/', views.scan_barcode, name='scan_barcode'),

    # API Routes
    path('api/events/', EventListAPIView.as_view(), name='api_event_list'),
    path('api/events/<int:pk>/', EventDetailAPIView.as_view(), name='api_event_detail'),
    path('api-token-auth/', CustomAuthToken.as_view(), name='custom_auth_token'),
]