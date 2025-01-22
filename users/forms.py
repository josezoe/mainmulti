from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.apps import apps
from django.forms.models import modelform_factory

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('users', 'CustomUser')
        fields = ['phone', 'country', 'state', 'city', 'preferred_currency', 'preferred_timezone', 'age', 'gender', 'income_level', 'housing_status', 'postal_code', 'lifestyle']
        widgets = {
            'interests': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your interests in JSON format', 'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['income_level'].queryset = apps.get_model('users', 'IncomeChoice').objects.none()
         self.fields['housing_status'].queryset = apps.get_model('users','HousingChoice').objects.none()
         if 'country' in self.data:
             try:
                 country_id = int(self.data.get('country'))
                 self.fields['income_level'].queryset = apps.get_model('users', 'IncomeChoice').objects.filter(country_id=country_id)
                 self.fields['housing_status'].queryset = apps.get_model('users','HousingChoice').objects.filter(country_id=country_id)
             except (ValueError, TypeError):
                 pass
         elif self.instance and self.instance.country_id:
              self.fields['income_level'].queryset = apps.get_model('users', 'IncomeChoice').objects.filter(country_id=self.instance.country_id)
              self.fields['housing_status'].queryset = apps.get_model('users','HousingChoice').objects.filter(country_id=self.instance.country_id)
         for field in self.fields:
             self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('users','CustomUser')
        fields = ['username', 'email', 'first_name', 'last_name', 'country', 'phone']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].queryset = apps.get_model('users', 'Country').objects.all()
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class UserSignupForm(UserCreationForm):
    class Meta:
        model = apps.get_model('users', 'CustomUser')
        fields = ('username', 'email', 'phone', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class UserPrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('users','UserPrivacySettings')
        fields = ['can_sell_data', 'can_target_ads', 'can_share_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-check-input'
            self.fields[field_name].label = f"Can we {field_name.replace('_', ' ')}?"

class PrivacyByDesignForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('users','PrivacyByDesign')
        fields = ['privacy_notice_accepted', 'data_minimized']
        widgets = {
           'data_minimized': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter minimized data fields in JSON format','class':'form-control'}),
       }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class IndianUserDataForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('users','IndianUserData')
        fields = ['consent_for_processing', 'data_purpose', 'data_lifecycle']
        widgets = {
            'data_lifecycle': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter data lifecycle in JSON format','class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class GDPRComplianceForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('users','GDPRCompliance')
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
        model = apps.get_model('users','UserConsent')
        fields = ['consented']

    def __init__(self, *args, **kwargs):
        consent_type = kwargs.pop('consent_type')
        user = kwargs.pop('user')
        super(ConsentForm, self).__init__(*args, **kwargs)
        try:
            instance = apps.get_model('users','UserConsent').objects.get(user=user, consent_type=consent_type)
            self.fields['consented'].initial = instance.consented
            self.instance = instance
        except apps.get_model('users','UserConsent').DoesNotExist:
            self.instance = apps.get_model('users','UserConsent')(user=user, consent_type=consent_type)
        self.fields['consented'].label = f"Do you consent to {consent_type.name}?"
        self.fields['consented'].widget.attrs['class'] = 'form-check-input'

class CCPAOptOutForm(forms.Form):
    opt_out = forms.BooleanField(required=False, label="Do Not Sell My Personal Information")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CCPAOptOutForm, self).__init__(*args, **kwargs)
        if user:
            try:
                privacy_settings = apps.get_model('users', 'UserPrivacySettings').objects.get(user=user)
                self.fields['opt_out'].initial = not privacy_settings.can_sell_data
            except apps.get_model('users', 'UserPrivacySettings').DoesNotExist:
                pass

class CCPAGlobalPrivacyControlForm(forms.Form):
    gpc = forms.BooleanField(required=False, label="Global Privacy Control (GPC)")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(CCPAGlobalPrivacyControlForm, self).__init__(*args, **kwargs)
        if request:
            self.fields['gpc'].initial = request.headers.get('Sec-GPC', '').lower() == 'true'

class VendorSignupForm(UserCreationForm):
    class Meta:
        model = apps.get_model('users', 'Vendor')
        fields = ['username', 'email', 'company_name', 'phone', 'country']

    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Password confirmation')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.user_type = 'vendor'  # Ensure user type is set to vendor
        if commit:
            user.save()
        return user

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('users','Vendor')
        fields = ['company_name', 'tax_id', 'contact_person_name', 'phone_number', 'business_email', 'website', 'address_line1', 'address_line2', 'direction', 'menu', 'cuisine_type', 'cuisines', 'opening_hours', 'description', 'about', 'facilities', 'atmosphere', 'spoken_languages', 'payment_options', 'special_conditions']
        
    def __init__(self, *args, **kwargs):
        super(VendorProfileForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

class VendorUpdateForm(forms.ModelForm):
    class Meta:
         model = apps.get_model('users','Vendor')
         fields = ['email', 'company_name', 'phone', 'country']

    def __init__(self, *args, **kwargs):
         super(VendorUpdateForm, self).__init__(*args, **kwargs)
         for field in self.fields:
             self.fields[field].widget.attrs.update({'class': 'form-control'})

class AdminVendorForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('users','Vendor')
        fields = ['username', 'email', 'company_name', 'phone', 'country', 'is_vendor_superuser']

    def __init__(self, *args, **kwargs):
        super(AdminVendorForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomUserAdminForm(UserChangeForm):
    class Meta:
        model = apps.get_model('users','CustomUser')
        fields = ('username', 'email', 'phone', 'country', 'state', 'city', 'preferred_currency', 'preferred_timezone', 'age', 'gender', 'income_level', 'housing_status', 'postal_code', 'lifestyle', 'user_type')
        
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomUserCreationForm(UserCreationForm):
    class Meta:
         model = apps.get_model('users','CustomUser')
         fields = ('username', 'email', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user

# New Forms for Roles and Permissions

class RoleForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('users', 'Role')
        fields = ['name', 'description', 'vendor']

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.fields['vendor'].queryset = apps.get_model('users', 'Vendor').objects.all()
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('users', 'UserRole')
        fields = ['user', 'role', 'vendor']

    def __init__(self, *args, **kwargs):
        super(UserRoleForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = apps.get_model('users', 'CustomUser').objects.all()
        self.fields['role'].queryset = apps.get_model('users', 'Role').objects.all()
        self.fields['vendor'].queryset = apps.get_model('users', 'Vendor').objects.all()
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class AppModuleForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('users', 'AppModule')
        fields = ['name', 'app_label', 'is_full_app']

    def __init__(self, *args, **kwargs):
        super(AppModuleForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})