from django import forms
from django.contrib.auth.models import User
from .models import CustomUser, UserPrivacySettings, PrivacyByDesign, IndianUserData, GDPRCompliance, UserConsent, ConsentType, Vendor
from django.contrib.auth.forms import UserCreationForm




class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['phone', 'country', 'state', 'city', 'preferred_currency', 'preferred_timezone', 'age', 'gender', 'income_level', 'housing_status', 'postal_code', 'lifestyle', 'interests']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['interests'].widget = forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your interests in JSON format'})

class UserSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email',)  # Add or remove fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
class UserPrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = UserPrivacySettings
        fields = ['can_sell_data', 'can_target_ads', 'can_share_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-check-input'
            self.fields[field_name].label = f"Can we {field_name.replace('_', ' ')}?"

class PrivacyByDesignForm(forms.ModelForm):
    class Meta:
        model = PrivacyByDesign
        fields = ['privacy_notice_accepted', 'data_minimized']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_minimized'].widget = forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter minimized data fields in JSON format'})

class IndianUserDataForm(forms.ModelForm):
    class Meta:
        model = IndianUserData
        fields = ['consent_for_processing', 'data_purpose', 'data_lifecycle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_lifecycle'].widget = forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter data lifecycle in JSON format'})

class GDPRComplianceForm(forms.ModelForm):
    class Meta:
        model = GDPRCompliance
        fields = ['has_access_right', 'has_rectification_right', 'has_erase_right', 'has_portability_right']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-check-input'
        self.fields['has_access_right'].label = "I want access to my personal data"
        self.fields['has_rectification_right'].label = "I want to rectify my personal data"
        self.fields['has_erase_right'].label = "I want to erase my personal data"
        self.fields['has_portability_right'].label = "I want to receive my data in a portable format"

class ConsentForm(forms.ModelForm):
    class Meta:
        model = UserConsent
        fields = ['consented']

    def __init__(self, *args, **kwargs):
        consent_type = kwargs.pop('consent_type')
        user = kwargs.pop('user')
        super(ConsentForm, self).__init__(*args, **kwargs)
        try:
            instance = UserConsent.objects.get(user=user, consent_type=consent_type)
            self.fields['consented'].initial = instance.consented
            self.instance = instance
        except UserConsent.DoesNotExist:
            self.instance = UserConsent(user=user, consent_type=consent_type)
        self.fields['consented'].label = f"Do you consent to {consent_type.name}?"
        self.fields['consented'].widget.attrs['class'] = 'form-check-input'

class CCPAOptOutForm(forms.Form):
    opt_out = forms.BooleanField(required=False, label="Do Not Sell My Personal Information")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CCPAOptOutForm, self).__init__(*args, **kwargs)
        if user:
            try:
                privacy_settings = UserPrivacySettings.objects.get(user=user)
                self.fields['opt_out'].initial = not privacy_settings.can_sell_data
            except UserPrivacySettings.DoesNotExist:
                pass

class CCPAGlobalPrivacyControlForm(forms.Form):
    gpc = forms.BooleanField(required=False, label="Global Privacy Control (GPC)")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(CCPAGlobalPrivacyControlForm, self).__init__(*args, **kwargs)
        if request:
            self.fields['gpc'].initial = request.headers.get('Sec-GPC', '').lower() == 'true'

class VendorSignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Password confirmation')

    class Meta:
        model = Vendor
        fields = ['username', 'email', 'company_name', 'phone', 'country']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['company_name', 'tax_id', 'contact_person_name', 'phone_number', 'business_email', 'website', 'address_line1', 'address_line2', 'direction', 'menu', 'cuisine_type', 'cuisines', 'opening_hours', 'description', 'about', 'facilities', 'atmosphere', 'spoken_languages', 'payment_options', 'special_conditions']
        
    def __init__(self, *args, **kwargs):
        super(VendorProfileForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

class VendorUpdateForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['email', 'company_name', 'phone', 'country']

    def __init__(self, *args, **kwargs):
        super(VendorUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class AdminVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['username', 'email', 'company_name', 'phone', 'country']

    def __init__(self, *args, **kwargs):
        super(AdminVendorForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

'''Concise Notes:
Profiles: Collect user details for segmentation and personalization.
Privacy Settings: User control over data use under privacy laws.
Privacy by Design: Ensure compliance with data minimization.
Indian Data: Consent and lifecycle for Indian privacy laws.
GDPR: Manage user rights under GDPR.
Consent: Track various consent types for compliance.
CCPA: Handle opt-out requests and GPC signals.
Vendor: Manage vendor registration and updates efficiently.'''