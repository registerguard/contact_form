#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.forms import widgets
from django.contrib.localflavor.us.forms import USStateField, USStateSelect, USPhoneNumberField, USZipCodeField
from django.conf import settings
from django.forms.fields import Select
from django.forms.util import ErrorList
from contact_form.forms import ContactForm

import datetime

class DeliveryContactForm(ContactForm):
    ROUTE_TYPES = (
        ('', 'Choose one ... '),
        ('Home delivery/Motor route', 'Home delivery/Motor route'),
        ('Contract bundle hauler', 'Contract bundle hauler'),
        ('Star Watch route (Tuesdays)', 'Star Watch route (Tuesdays)'),
        ('Contract single copy delivery', 'Contract single copy delivery'),
        ('Substitute carrier', 'Substitute carrier'),
        ('Specific advertised route (specify which in comment box below)', 'Specific advertised route (specify which in comment box below)'),
    )
    
    address = forms.CharField(max_length = 175)
    apt_no = forms.CharField(max_length = 10, required = False, label=u'Apartment no.')
    po_box = forms.CharField(max_length = 15, required = False, label=u'P.O. Box')
    city = forms.CharField(max_length = 75)
    zip = forms.CharField(max_length = 25, label=u'ZIP')
    telephone = forms.CharField(max_length = 12)
    route_type = forms.ChoiceField(choices = ROUTE_TYPES)
    body = forms.CharField(widget=forms.Textarea(),
                              label=u'Enter any comments below that may help us better process your request.',
                              required=False)
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(),
                           label=u'Name')
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(maxlength=200)),
                             label=u'E-mail address')
    recipient_list = ['dispatch@registerguard.com', 'john.heasly@registerguard.com', ]

    def from_email(self):
        if self.is_valid():
            return self.cleaned_data['email']

class ClassifiedsSearchContactForm(ContactForm):
    body = forms.CharField(widget=forms.Textarea(),
                              label=u'If describing something you believe is broken, please be as specific as possible regarding the circumstances of the error',)
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(),
                           label=u'Name')
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(maxlength=200)),
                             label=u'E-mail address')
    recipient_list = ['searchfeedback@registerguard.com', 'john.heasly@registerguard.com', ]
    subject_template_name = 'contact_form/contact_form_subject_classifieds_search.txt'
    template_name =         'contact_form/contact_form_classifieds_search.txt'
    
    def from_email(self):
        if self.is_valid():
            return self.cleaned_data['email']

class FlagContactForm(ContactForm):
    body = forms.CharField(widget=forms.Textarea(),
                             label=u'Any comments (optional)',
                             required=False)
    recipient_list = ['webeditors@registerguard.com']
    
    cms_id = forms.CharField(required=False, widget=forms.HiddenInput())
    
    comment_id = forms.CharField(required=False, widget=forms.HiddenInput())
    
    refering_url = forms.CharField(required=False, widget=forms.HiddenInput())
    
    subject_template_name = 'contact_form/contact_form_subject_flag.txt'
    template_name =         'contact_form/contact_form_flag.txt'
    
    def from_email(self):
        if self.is_valid():
            return self.cleaned_data['email']

class HackedUSStateSelect(Select):
    def __init__(self, attrs=None):
        from django.contrib.localflavor.us.us_states import STATE_CHOICES
        MY_STATE_CHOICES = (('', u'---------'),) + STATE_CHOICES + ((u'OS', u'Outside the U.S.'),)
        super(HackedUSStateSelect, self).__init__(attrs, choices=MY_STATE_CHOICES)

class CalendarWidget(forms.DateInput):
    class Media:
#         css = {'all':('http://ajax.googleapis.com/ajax/libs/jqueryui/1/themes/overcast/jquery-ui.css',)}
        css = {'all':('http://projects.registerguard.com/static/wedding-form/css/fm_wedding_announcement/jquery-ui-1.8.13.custom.css',)}
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1/jquery-ui.min.js',
        )

class WeddingForm(ContactForm):
    recipient_list = [
    'john.heasly@registerguard.com', 
    'rob.denton@registerguard.com', 
    'weddings@registerguard.com',
#     'cjw@registerguard.com',
#     'carl.davaz@registerguard.com', 
#     'chris.frisella@registerguard.com', 
#     'jan.lafeman@registerguard.com', 
#     'ian.doremus@registerguard.com',
    ]
    
    subject_template_name = 'contact_form/contact_form_wedding_subject.txt'
    template_name =         'contact_form/contact_form_wedding.txt'
    
    YES_NO = (
        (True, 'Yes',),
        (False, 'No',),
    )
    BRIDE_GROOM = (
        ('Bride', 'Bride only',),
        ('Both', 'Both bride and bridegroom',),
    )
    
    from django.contrib.localflavor.us.us_states import STATE_CHOICES
    MY_STATE_CHOICES = (('', u'---------'),) + STATE_CHOICES + ((u'Outside the U.S.', u'Outside the U.S.'),)
        
    # Hack to hide inherited ContactForm fields
    body = forms.CharField(required=False, widget=forms.HiddenInput())
    name = forms.CharField(required=False, widget=forms.HiddenInput())
    
    email = forms.EmailField(max_length=200, label=u'Your e-mail address')
    
    bride_name_first = forms.CharField(label=u'Bride\'s first name', initial='Bride\'s first name', max_length=100)
    bride_name_last = forms.CharField(label=u'Bride\'s maiden name', initial='Bride\'s maiden name', max_length=100)
    bride_work_phone = USPhoneNumberField(label=u'Bride\'s work phone', help_text='(XXX-XXX-XXXX format)')
    bride_home_phone = USPhoneNumberField(label=u'Bride\'s home phone', help_text='(XXX-XXX-XXXX format)')
    bride_city = forms.CharField(label=u'Bride\'s city')
    bride_state = forms.ChoiceField(widget=HackedUSStateSelect(), choices=MY_STATE_CHOICES, label=u'Bride\'s state', initial='OR')
    groom_name_first = forms.CharField(label=u'Bridegroom\'s first name', initial='Groom\'s first name', max_length=100)
    groom_name_last = forms.CharField(label=u'Bridegroom\'s last name', initial='Groom\'s last name', max_length=100)
    groom_work_phone = USPhoneNumberField(label=u'Bridegroom\'s work phone', help_text='(XXX-XXX-XXXX format)')
    groom_home_phone = USPhoneNumberField(label=u'Bridegroom\'s home phone', help_text='(XXX-XXX-XXXX format)')
    groom_city = forms.CharField(label=u'Bridegroom\'s city')
    groom_state = forms.ChoiceField(widget=HackedUSStateSelect(), choices=MY_STATE_CHOICES, label=u'Bridegroom\'s state', initial='OR')
    wedding_date = forms.DateField(help_text=u'Date should be today or later, but no more than 90 days ago.', widget=CalendarWidget())
    wedding_location = forms.CharField(help_text='(Include facility, city and state)')
    brides_parents_married = forms.ChoiceField(
        widget=forms.RadioSelect(), 
        choices=YES_NO, 
        label=u'Bride\'s parents',
        help_text='Divorced?',
    )
    brides_mother_living = forms.ChoiceField(
        widget=forms.RadioSelect(), 
        choices=YES_NO, 
        label=u'Bride\'s mother',
        help_text='Deceased?',
    )
    brides_father_living = forms.ChoiceField(
        widget=forms.RadioSelect(), 
        choices=YES_NO, 
        label=u'Bride\'s father',
        help_text='Deceased?',
    )
    brides_mother_name = forms.CharField(label=u'Bride\'s mother\'s name (and name of spouse if remarried)', help_text=u'(Use first and last names.)')
    brides_mother_city = forms.CharField(label=u'Bride\'s mother\'s city')
    brides_mother_state = forms.ChoiceField(widget=HackedUSStateSelect(), choices=MY_STATE_CHOICES, label=u'Bride\'s mother\'s state')
    brides_mother_day_phone = forms.CharField(required=False, label=u'Bride\'s mother\'s daytime phone', help_text='(XXX-XXX-XXXX format)')
    brides_father_name = forms.CharField(label=u'Bride\'s father\'s name (and name of spouse if remarried)', help_text=u'(Use first and last names.)')
    brides_father_city = forms.CharField(label=u'Bride\'s father\'s city')
    brides_father_state = forms.ChoiceField(widget=HackedUSStateSelect(), choices=MY_STATE_CHOICES, label=u'Bride\'s father\'s state')
    brides_father_day_phone = forms.CharField(required=False, label=u'Bride\'s father\'s daytime phone', help_text='(XXX-XXX-XXXX format)')
    
    grooms_parents_married = forms.ChoiceField(
        widget=forms.RadioSelect(), 
        choices=YES_NO, 
        label=u'Bridegroom\'s parents',
        help_text='Divorced?',
    )
    grooms_mother_living = forms.ChoiceField(
        widget=forms.RadioSelect(), 
        choices=YES_NO, 
        label=u'Bridegroom\'s mother',
        help_text='Deceased?',
    )
    grooms_father_living = forms.ChoiceField(
        widget=forms.RadioSelect(), 
        choices=YES_NO, 
        label=u'Bridegroom\'s father',
        help_text='Deceased?',
    )
    grooms_mother_name = forms.CharField(label=u'Bridegroom\'s mother\'s name (and name of spouse if remarried)', help_text=u'(Use first and last names.)')
    grooms_mother_city = forms.CharField(label=u'Bridegroom\'s mother\'s city')
    grooms_mother_state = forms.ChoiceField(widget=HackedUSStateSelect(), choices=MY_STATE_CHOICES,  label=u'Bridegroom\'s mother\'s state')
    grooms_mother_day_phone = forms.CharField(required=False, label=u'Bridegroom\'s mother\'s daytime phone', help_text='(XXX-XXX-XXXX format)')
    grooms_father_name = forms.CharField(label=u'Bridegroom\'s father\'s name (and name of spouse if remarried)', help_text=u'(Use first and last names.)')
    grooms_father_city = forms.CharField(label=u'Bridegroom\'s father\'s city')
    grooms_father_state = forms.ChoiceField(widget=HackedUSStateSelect(), choices=MY_STATE_CHOICES, label=u'Bridegroom\'s father\'s state')
    grooms_father_day_phone = forms.CharField(required=False, label=u'Bridegroom\'s father\'s daytime phone', help_text='(XXX-XXX-XXXX format)')
    
    couples_future_home = forms.CharField(label=u'Couple\'s future home')
    brides_occupation = forms.CharField(label=u'Bride\'s occupation')
    grooms_occupation = forms.CharField(label=u'Bridegroom\'s occupation')
    
    bride_maiden_name = forms.ChoiceField(
        widget=forms.RadioSelect(), 
        choices=YES_NO, 
        label=u'Will the bride be keeping her maiden name as her last name?',
    )
    last_name_hyphenated = forms.ChoiceField(
        widget=forms.RadioSelect(), 
        choices=YES_NO, 
        label=u'Will the last name be hyphenated?',
    )
    hyphenation = forms.CharField(label=u'If so, show how', required=False)
    hyphenation_who = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect(), 
        choices=BRIDE_GROOM, 
        label=u'Hyphenated last name be used by',
    )
    photo = forms.ImageField(help_text='(2MB maximum file size; file sizes of at least 500KB with a moderately tight crop of the couple i.e., from waist up, work best.)')
    comments = forms.CharField(widget=forms.Textarea(attrs={'rows': '3'}), label=u'Optional comments', required=False, help_text='Anything else we should know?')
    
    def from_email(self):
        if self.is_valid():
            return self.cleaned_data['email']
    
    def clean_wedding_date(self):
        from django.template.defaultfilters import date
        
        data = self.cleaned_data['wedding_date']
        if data > datetime.date.today():
            raise forms.ValidationError('Wedding announcement forms are only accepted after the wedding date has passed and for 90 days thereafter. Please submit at that time. We apologize for any inconvenience. Thank you.')
        
        formatted_data = date(data, 'N j')
        return formatted_data
    
    def clean_photo(self):
        if self.is_valid():
            image = self.cleaned_data['photo']
            if image.size > 2048000: # 2MB = 2048000 bytes
                raise forms.ValidationError('Photo file too big; file size exceeds 2MB')
            elif image.size < 512000:
                raise forms.ValidationError('Photo file size not large enough; photo file size must be at least 500KB.')
            
            self.cleaned_data['org_ext'] = image.name.split('.')[-1]
            return image

class EnhancedSplitDateTimeWidget(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None):
        widgets.MultiWidget.__init__(self, widgets=(forms.DateInput(attrs={ 'class': 'datePicker p25' }),
                                                    forms.TimeInput(attrs={ 'class': 'timePicker p25' })), attrs=attrs)
    
    class Media:
        css = {
            'all': ('http://assets.registerguard.com/v3.5/css/registerguard.css?v=070109',
                    'http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/base/jquery-ui.css',),
        }
        js = (
            'http://rg-assets.s3.amazonaws.com/v3.5/js/jquery.min.js', 
            'http://rg-assets.s3.amazonaws.com/v3.5/js/jquery-ui.min.js', 
#             'http://rg-assets.s3.amazonaws.com/v3.5/js/jquery.timepicker.basic.js', 
            'http://assets.registerguard.com/v3.5/js/jquery.timepicker.basic.js', 
            'http://rg-assets.s3.amazonaws.com/v3.5/js/registerguard.js?v=111209x', 
        )

class DeathNoticeForm(forms.Form):
    SERVICES = (
        ('', '----',),
        ('celebration of life', 'celebration of life',),
        ('funeral', 'funeral',),
        ('memorial service', 'memorial service',),
    )
    deceased_first_name = forms.CharField(label=u'Deceased\'s first name', help_text=u'Include middle initial or nickname in quotations, if desired.')
    deceased_last_name = forms.CharField(label=u'Deceased\'s last name')
    age = forms.IntegerField()
    city = forms.CharField(label=u'Deceased\'s city')
    death_date = forms.DateField(label=u'Date of death', 
        widget=forms.DateInput(attrs={ 'class': 'datePicker p25'}), )
    service = forms.ChoiceField(choices=SERVICES, required=False, label=u'Type of service, if any')
    service_date_time = forms.SplitDateTimeField(required=False, label=u'If service, indicate date and time', input_time_formats=('%I:%M %p',), widget=EnhancedSplitDateTimeWidget() )
    service_location = forms.CharField(required=False)
    service_city = forms.CharField(required=False)
    arrangements = forms.CharField(label=u'Arrangements by')
    arrangements_city = forms.CharField(initial=u'Eugene', label=u'City where funeral home is located.')
    
    def clean(self):
        cleaned_data = self.cleaned_data
        service = cleaned_data.get('service')
        service_date_time = cleaned_data.get('service_date_time')
        service_location = cleaned_data.get('service_location')
        service_city = cleaned_data.get('service_city')
        
        service_fields = (service, service_date_time, service_location, service_city,)
        
        if any(service_fields):
            if not all(service_fields):
                msg = u'All service fields must be completed: "Type of service", "Service date and time", "Service location" and "Service city".'
                self._errors['service'] = ErrorList([msg])
        return cleaned_data

class ObituaryForm(forms.Form):
    GENDERS = (
        ('',   '----',),
        ('Male',   'M',),
        ('Female', 'F',),
    )
    sex = forms.ChoiceField(choices=GENDERS)
    length_residence = forms.CharField(label=u'Length of residence in Lane County area')
    dob = forms.DateField(label=u'Date of birth',
        widget = forms.DateInput(attrs={ 'class': 'datePicker p25' }), )
    birthplace = forms.CharField(label=u'Place of birth')
    parents_names = forms.CharField(label=u'Parents\' names, mother\'s maiden name in parentheses', initial='John and Mary (Smith) Jones')
    cause_death = forms.CharField(label=u'Cause of death')
    no_service = forms.BooleanField(label=u'Check if no service planned')
    visitation = forms.CharField(required=False)
    visitation_location = forms.CharField(required=False)
