from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.db.models import Q, Count, Sum, F, Avg, Max, Min, ExpressionWrapper, FloatField, DateTimeField
from django.utils import timezone
from django import forms
from django.utils.html import format_html
from django.core.cache import cache
from django.db.models.functions import TruncMonth, TruncDay, Extract
import json
from .models import CustomUser,Currency, Vendor, UserPrivacySettings, PrivacyByDesign, IndianUserData, GDPRCompliance, UserConsent, ConsentType, Country, Timezone, State, City, Tax

# Custom Date Range Filter
class DateRangeFilter(SimpleListFilter):
    title = _('Date Range')
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return [
            ('today', _('Today')),
            ('yesterday', _('Yesterday')),
            ('this_week', _('This Week')),
            ('last_week', _('Last Week')),
            ('this_month', _('This Month')),
            ('last_month', _('Last Month')),
            ('custom', _('Custom Range')),
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        now = timezone.now()
        if self.value() == 'today':
            return queryset.filter(last_visit__date=now.date())
        elif self.value() == 'yesterday':
            return queryset.filter(last_visit__date=now.date() - timezone.timedelta(days=1))
        elif self.value() == 'this_week':
            return queryset.filter(last_visit__date__gte=now - timezone.timedelta(days=now.weekday()), last_visit__date__lte=now)
        elif self.value() == 'last_week':
            last_week_start = now - timezone.timedelta(days=now.weekday() + 7)
            last_week_end = last_week_start + timezone.timedelta(days=6)
            return queryset.filter(last_visit__date__gte=last_week_start, last_visit__date__lte=last_week_end)
        elif self.value() == 'this_month':
            return queryset.filter(last_visit__year=now.year, last_visit__month=now.month)
        elif self.value() == 'last_month':
            last_month = now - timezone.timedelta(days=now.day)
            return queryset.filter(last_visit__year=last_month.year, last_visit__month=last_month.month)
        elif self.value() == 'custom':
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if start_date and end_date:
                return queryset.filter(last_visit__date__gte=start_date, last_visit__date__lte=end_date)

        return queryset

# Custom Location Filter
class LocationFilter(SimpleListFilter):
    title = _('Location')
    parameter_name = 'location'

    def lookups(self, request, model_admin):
        locations = []
        countries = model_admin.model.objects.values_list('country__name', flat=True).distinct()
        for country in countries:
            locations.append((f'country_{country}', country))
            states = model_admin.model.objects.filter(country__name=country).values_list('state__name', flat=True).distinct()
            for state in states:
                locations.append((f'state_{state}', f'-- {state}'))
                cities = model_admin.model.objects.filter(state__name=state).values_list('city__name', flat=True).distinct()
                for city in cities:
                    locations.append((f'city_{city}', f'---- {city}'))
        return locations

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            if value.startswith('country_'):
                return queryset.filter(country__name=value[8:])
            elif value.startswith('state_'):
                return queryset.filter(state__name=value[6:])
            elif value.startswith('city_'):
                return queryset.filter(city__name=value[5:])
        return queryset

# Custom Cohort Filter
class CohortFilter(SimpleListFilter):
    title = _('Cohort')
    parameter_name = 'cohort'

    def lookups(self, request, model_admin):
        months = CustomUser.objects.annotate(month=TruncMonth('date_joined')).values_list('month', flat=True).distinct().order_by('-month')
        return [(month.strftime('%Y-%m'), month.strftime('%B %Y')) for month in months]

    def queryset(self, request, queryset):
        if self.value():
            cohort = timezone.datetime.strptime(self.value(), "%Y-%m").date()
            return queryset.filter(date_joined__year=cohort.year, date_joined__month=cohort.month)
        return queryset

# Inline for Privacy Settings
class PrivacySettingsInline(admin.TabularInline):
    model = UserPrivacySettings
    can_delete = False
    fields = ('can_sell_data', 'can_target_ads', 'can_share_data')
    verbose_name_plural = _('Privacy Settings')

# Inline for Privacy By Design
class PrivacyByDesignInline(admin.TabularInline):
    model = PrivacyByDesign
    can_delete = False
    fields = ('privacy_notice_accepted', 'data_minimized')
    verbose_name_plural = _('Privacy By Design')

# Inline for Indian User Data
class IndianUserDataInline(admin.TabularInline):
    model = IndianUserData
    can_delete = False
    fields = ('consent_for_processing', 'data_purpose', 'data_lifecycle')
    verbose_name_plural = _('Indian User Data')

# Inline for GDPR Compliance
class GDPRComplianceInline(admin.TabularInline):
    model = GDPRCompliance
    can_delete = False
    fields = ('has_access_right', 'has_rectification_right', 'has_erase_right', 'has_portability_right')
    verbose_name_plural = _('GDPR Compliance')

# Inline for User Consent
class UserConsentInline(admin.TabularInline):
    model = UserConsent
    fields = ('consent_type', 'consented', 'date_consented', 'date_withdrawn')
    verbose_name_plural = _('Consents')

# Custom User Admin with advanced search, location filter, and privacy/compliance inlines
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'country', 'state', 'city', 'age', 'gender', 'income_level', 'segment', 'last_visit', 'visit_count', 'total_visits', 'total_spent', 'engagement_score', 'retention_status', 'days_since_last_visit', 'lifetime_value', 'session_length', 'visit_frequency', 'net_promoter_score')
    search_fields = ['username', 'email', 'phone', 'country__name', 'state__name', 'city__name', 'interests']
    list_filter = (
        'user_type',
        LocationFilter,
        'age',
        'gender',
        'income_level',
        'segment',
        'lifestyle',
        'last_purchase_date',
        'purchase_count',
        DateRangeFilter,
        CohortFilter,
    )
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal Information'), {'fields': ('phone', 'country', 'state', 'city', 'age', 'gender')}),
        (_('Preferences'), {'fields': ('preferred_currency', 'preferred_timezone', 'income_level', 'housing_status', 'postal_code')}),
        (_('Segmentation Data'), {'fields': ('lifestyle', 'interests')}),
        (_('Behavioral Analytics'), {'fields': ('last_page_visited', 'visit_count', 'last_visit', 'search_history', 'purchase_history')}),
        (_('RFM Metrics'), {'fields': ('last_purchase_date', 'purchase_count', 'total_spent', 'segment')}),
    )

    inlines = [PrivacySettingsInline, PrivacyByDesignInline, IndianUserDataInline, GDPRComplianceInline, UserConsentInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_type='customer')

    def total_visits(self, obj):
        return obj.visit_count
    total_visits.short_description = _('Total Visits')

    def total_spent(self, obj):
        return obj.total_spent if obj.total_spent else '0.00'
    total_spent.short_description = _('Total Spent')

    def engagement_score(self, obj):
        engagement = obj.visit_count * 0.3 + obj.purchase_count * 0.5 + (obj.total_spent / 1000) * 0.2
        return f"{engagement:.2f}"
    engagement_score.short_description = _('Engagement Score')

    def retention_status(self, obj):
        now = timezone.now().date()
        if obj.last_purchase_date and (now - obj.last_purchase_date.date()).days <= 30:
            return _('Active')
        elif obj.last_visit and (now - obj.last_visit.date()).days <= 90:
            return _('Medium')
        elif obj.last_visit and (now - obj.last_visit.date()).days > 90:
            return _('Low')
        else:
            return _('Never Engaged')
    retention_status.short_description = _('Retention Status')

    def days_since_last_visit(self, obj):
        if obj.last_visit:
            return (timezone.now().date() - obj.last_visit.date()).days
        return None
    days_since_last_visit.short_description = _('Days Since Last Visit')

    def lifetime_value(self, obj):
        return obj.total_spent * (1 + obj.purchase_count)
    lifetime_value.short_description = _('Lifetime Value')

    def session_length(self, obj):
        return f"{obj.session_length / 60:.2f} minutes" if obj.session_length else '0.00 minutes'
    session_length.short_description = _('Avg Session Length')

    def visit_frequency(self, obj):
        if obj.last_visit:
            days_since_registration = (timezone.now().date() - obj.date_joined.date()).days
            return obj.visit_count / days_since_registration if days_since_registration > 0 else obj.visit_count
        return 0
    visit_frequency.short_description = _('Visit Frequency (per day)')

    def net_promoter_score(self, obj):
        return obj.nps or 'N/A'
    net_promoter_score.short_description = _('NPS')

    def get_search_results(self, request, queryset, search_term):
        qs, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            qs = qs.filter(
                Q(username__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(phone__icontains=search_term) |
                Q(country__name__icontains=search_term) |
                Q(state__name__icontains=search_term) |
                Q(city__name__icontains=search_term) |
                Q(interests__contains=search_term)
            )
        return qs, use_distinct

    def changelist_view(self, request, extra_context=None):
        if 'date_range' in request.GET and request.GET['date_range'] == 'custom':
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if start_date and end_date:
                extra_context = extra_context or {}
                extra_context['start_date'] = start_date
                extra_context['end_date'] = end_date

        # Add summary statistics for behavior, engagement, retention, and additional metrics
        extra_context = extra_context or {}
        extra_context['summary'] = self.get_summary_data(request)
        extra_context['engagement_stats'] = self.get_engagement_stats(request)
        extra_context['retention_stats'] = self.get_retention_stats(request)
        extra_context['ltv_stats'] = self.get_ltv_stats(request)
        extra_context['session_stats'] = self.get_session_stats(request)
        extra_context['nps_stats'] = self.get_nps_stats(request)
        extra_context['cohort_stats'] = self.get_cohort_stats(request)
        extra_context['churn_stats'] = self.get_churn_stats(request)

        return super().changelist_view(request, extra_context=extra_context)

    def get_summary_data(self, request):
        cache_key = 'behavior_summary'
        summary = cache.get(cache_key)
        if summary is None:
            qs = self.get_queryset(request)
            summary = {
                'total_users': qs.count(),
                'total_visits': qs.aggregate(total=Sum('visit_count'))['total'] or 0,
                'total_spent': qs.aggregate(total=Sum('total_spent'))['total'] or 0,
                'most_visited_page': qs.values('last_page_visited').annotate(count=Count('last_page_visited')).order_by('-count').first(),
                'top_segments': qs.values('segment').annotate(count=Count('id')).order_by('-count')[:5],
            }
            cache.set(cache_key, summary, 60 * 5)  # Cache for 5 minutes
        return summary

    def get_engagement_stats(self, request):
        cache_key = 'engagement_stats'
        stats = cache.get(cache_key)
        if stats is None:
            qs = self.get_queryset(request)
            stats = {
                'average_engagement': qs.aggregate(avg=Avg(F('visit_count') * 0.3 + F('purchase_count') * 0.5 + (F('total_spent') / 1000) * 0.2))['avg'] or 0,
                'high_engagement_users': qs.filter(visit_count__gte=10, purchase_count__gte=3).count(),  # Arbitrary thresholds
            }
            cache.set(cache_key, stats, 60 * 5)  # Cache for 5 minutes
        return stats

    def get_retention_stats(self, request):
        cache_key = 'retention_stats'
        stats = cache.get(cache_key)
        if stats is None:
            qs = self.get_queryset(request)
            now = timezone.now().date()
            stats = {
                'active_users': qs.filter(last_purchase_date__gte=now - timezone.timedelta(days=30)).count(),
                'medium_retention': qs.filter(last_visit__gte=now - timezone.timedelta(days=90)).exclude(last_purchase_date__gte=now - timezone.timedelta(days=30)).count(),
                'low_retention': qs.filter(last_visit__lt=now - timezone.timedelta(days=90)).count(),
                'monthly_retention_rate': self.calculate_monthly_retention_rate(qs),
            }
            cache.set(cache_key, stats, 60 * 5)  # Cache for 5 minutes
        return stats

    def get_ltv_stats(self, request):
        cache_key = 'ltv_stats'
        ltv_stats = cache.get(cache_key)
        if ltv_stats is None:
            qs = self.get_queryset(request)
            ltv_stats = {
                'average_ltv': qs.aggregate(avg=Avg(F('total_spent') * (F('purchase_count') + 1)))['avg'] or 0,
                'high_ltv_users': qs.filter(total_spent__gte=500).count(),  # Arbitrary high LTV threshold
            }
            cache.set(cache_key, ltv_stats, 60 * 5)  # Cache for 5 minutes
        return ltv_stats

    def get_session_stats(self, request):
        cache_key = 'session_stats'
        stats = cache.get(cache_key)
        if stats is None:
            qs = self.get_queryset(request)
            stats = {
                'average_session': qs.aggregate(avg=Avg('session_length'))['avg'] or 0,
                'longest_session': qs.aggregate(max=Max('session_length'))['max'] or 0,
            }
            cache.set(cache_key, stats, 60 * 5)  # Cache for 5 minutes
        return stats

    def get_nps_stats(self, request):
        cache_key = 'nps_stats'
        stats = cache.get(cache_key)
        if stats is None:
            qs = self.get_queryset(request)
            stats = {
                'average_nps': qs.aggregate(avg=Avg('nps'))['avg'] or 0,
                'promoters': qs.filter(nps__gte=9).count(),
                'detractors': qs.filter(nps__lte=6).count(),
            }
            cache.set(cache_key, stats, 60 * 5)  # Cache for 5 minutes
        return stats

    def get_cohort_stats(self, request):
        cache_key = 'cohort_stats'
        stats = cache.get(cache_key)
        if stats is None:
            qs = self.get_queryset(request)
            today = timezone.now()
            stats = {}
            for month in qs.annotate(month=TruncMonth('date_joined')).values_list('month', flat=True).distinct().order_by('-month'):
                cohort = qs.filter(date_joined__year=month.year, date_joined__month=month.month)
                stats[month.strftime('%B %Y')] = {
                    'size': cohort.count(),
                    'retention': cohort.filter(last_visit__gte=today - timezone.timedelta(days=30)).count() / cohort.count() if cohort.count() > 0 else 0
                }
            cache.set(cache_key, stats, 60 * 5)  # Cache for 5 minutes
        return stats

    def get_churn_stats(self, request):
        cache_key = 'churn_stats'
        stats = cache.get(cache_key)
        if stats is None:
            qs = self.get_queryset(request)
            last_month = (timezone.now() - timezone.timedelta(days=30)).date()
            this_month = timezone.now().date()
            active_last_month = qs.filter(last_visit__gte=last_month, last_visit__lt=this_month).count()
            active_this_month = qs.filter(last_visit__gte=this_month).count()
            stats = {
                'monthly_churn_rate': ((active_last_month - active_this_month) / active_last_month) * 100 if active_last_month > 0 else 0
            }
            cache.set(cache_key, stats, 60 * 5)  # Cache for 5 minutes
        return stats

    def calculate_monthly_retention_rate(self, qs):
        last_month = (timezone.now() - timezone.timedelta(days=30)).date()
        users_last_month = qs.filter(last_visit__gte=last_month).count()
        if users_last_month == 0:
            return 0
        return (qs.filter(last_visit__gte=timezone.now().date()).count() / users_last_month) * 100

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'date_range' in request.GET and request.GET['date_range'] == 'custom':
            form.base_fields['start_date'] = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
            form.base_fields['end_date'] = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
        return form

    def display_summary(self, obj):
        summary = self.get_summary_data(obj)
        engagement_stats = self.get_engagement_stats(obj)
        retention_stats = self.get_retention_stats(obj)
        ltv_stats = self.get_ltv_stats(obj)
        session_stats = self.get_session_stats(obj)
        nps_stats = self.get_nps_stats(obj)
        cohort_stats = self.get_cohort_stats(obj)
        churn_stats = self.get_churn_stats(obj)

        cohort_list = ''.join([f'<li>{cohort}: Size {data["size"]}, Retention {data["retention"]:.2f}</li>' for cohort, data in cohort_stats.items()])

        return format_html("""
            <div>
                <h4>Behavior Analytics Summary</h4>
                <p>Total Users: {}</p>
                <p>Total Visits: {}</p>
                <p>Total Spent: ${}</p>
                <p>Most Visited Page: {}</p>
                <p>Top Segments:</p>
                <ul>{}</ul>
                
                <h4>Engagement Stats</h4>
                <p>Average Engagement Score: {:.2f}</p>
                <p>High Engagement Users: {}</p>
                
                <h4>Retention Stats</h4>
                <p>Active Users (last 30 days): {}</p>
                <p>Medium Retention (last 90 days): {}</p>
                <p>Low Retention: {}</p>
                <p>Monthly Retention Rate: {:.2f}%</p>
                
                <h4>Lifetime Value Stats</h4>
                <p>Average LTV: ${:.2f}</p>
                <p>High LTV Users: {}</p>
                
                <h4>Session Stats</h4>
                <p>Average Session Length: {:.2f} min</p>
                <p>Longest Session: {:.2f} min</p>
                
                <h4>NPS Stats</h4>
                <p>Average NPS: {:.2f}</p>
                <p>Promoters: {}</p>
                <p>Detractors: {}</p>
                
                <h4>Cohort Stats</h4>
                <ul>{}</ul>
                
                <h4>Churn Stats</h4>
                <p>Monthly Churn Rate: {:.2f}%</p>
            </div>
        """, 
        summary['total_users'], 
        summary['total_visits'], 
        summary['total_spent'],
        summary['most_visited_page']['last_page_visited'] if summary['most_visited_page'] else 'None',
        ''.join([f'<li>{segment["segment"]}: {segment["count"]}</li>' for segment in summary['top_segments']]),
        engagement_stats['average_engagement'],
        engagement_stats['high_engagement_users'],
        retention_stats['active_users'],
        retention_stats['medium_retention'],
        retention_stats['low_retention'],
        retention_stats['monthly_retention_rate'],
        ltv_stats['average_ltv'],
        ltv_stats['high_ltv_users'],
        session_stats['average_session'] / 60 if session_stats['average_session'] else 0,
        session_stats['longest_session'] / 60 if session_stats['longest_session'] else 0,
        nps_stats['average_nps'],
        nps_stats['promoters'],
        nps_stats['detractors'],
        cohort_list,
        churn_stats['monthly_churn_rate'])

    display_summary.short_description = _('Summary')
    display_summary.allow_tags = True


# Vendor Admin with similar filters
class VendorAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'company_name', 'country', 'state', 'city', 'average_rating', 'review_count', 'is_vendor_superuser')
    search_fields = ['username', 'email', 'company_name', 'contact_person_name', 'phone_number', 'business_email', 'website', 'address_line1', 'cuisine_type', 'spoken_languages']
    list_filter = (
        LocationFilter,
        'cuisine_type',
        'created_at',
        'is_vendor_superuser',
        DateRangeFilter,
    )
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Vendor Information'), {'fields': ('company_name', 'tax_id', 'contact_person_name', 'phone_number', 'business_email', 'website')}),
        (_('Address'), {'fields': ('country', 'state', 'city', 'address_line1', 'address_line2', 'postal_code', 'direction')}),
        (_('Operational'), {'fields': ('menu', 'cuisine_type', 'cuisines', 'opening_hours', 'description', 'about', 'facilities', 'atmosphere', 'spoken_languages', 'payment_options', 'special_conditions')}),
        (_('Review'), {'fields': ('average_rating', 'review_count')}),
        (_('Timestamp'), {'fields': ('created_at', 'updated_at')}),
        (_('Permissions'), {'fields': ('is_vendor_superuser',)}),
    )

    def get_search_results(self, request, queryset, search_term):
        qs, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            qs = qs.filter(
                Q(username__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(company_name__icontains=search_term) |
                Q(contact_person_name__icontains=search_term) |
                Q(phone_number__icontains=search_term) |
                Q(business_email__icontains=search_term) |
                Q(website__icontains=search_term) |
                Q(address_line1__icontains=search_term) |
                Q(cuisine_type__icontains=search_term)
            )
        return qs, use_distinct

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_type='vendor')

    def changelist_view(self, request, extra_context=None):
        return CustomUserAdmin.changelist_view(self, request, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        return CustomUserAdmin.get_form(self, request, obj, **kwargs)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Vendor, VendorAdmin)


def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request)

    # Group Users & Vendor Under "Links"
    links_app = {
        "name": "Links",
        "app_label": "links_app",  # Unique label to avoid clash
        "models": []
    }
    
    for app in list(app_dict.values()):
        for model in app['models']:
            if model['admin_url'].endswith('/users/customuser/') or model['admin_url'].endswith('/users/vendor/'):
               links_app['models'].append(model)
               app_dict.pop(app["app_label"])
    
    if links_app['models']:
        app_dict['links_app'] = links_app

    return sorted(app_dict.values(), key=lambda app: app['name'])



# Register models in admin
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'currency', 'default_timezone']
    
@admin.register(Timezone)
class TimezoneAdmin(admin.ModelAdmin):
    list_display = ['name']
    
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name','country','timezone']
    list_filter = ['country','timezone']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state']
    list_filter = ['state']

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage','state']
    list_filter = ['state']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'symbol']
    list_filter = ['name', 'code', 'symbol']
    search_fields = ['name', 'code', 'symbol']
