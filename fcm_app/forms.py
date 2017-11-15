from django import forms
from ckeditor.widgets import CKEditorWidget
from django_countries.widgets import CountrySelectWidget
from django_countries import countries
import calendar
from .models import FCM


STATUS_CHOICES= [
    ('1', 'Public'),
    ('2', 'Private'),
    ]

class FCMForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'cols': '50'}))
    country = forms.ChoiceField(label = 'Country', initial = 'GR', widget = CountrySelectWidget(attrs={'class': 'form-control'}), choices=countries)
    status = forms.IntegerField(label='Status', initial = 1, widget= forms.RadioSelect(choices = STATUS_CHOICES))
    map_image = forms.FileField(label='Image', widget=forms.FileInput())
    map_html = forms.FileField(label='HTML', widget=forms.FileInput)

class FCMCONCEPTForm(forms.Form):
    concept_info = forms.CharField(widget=CKEditorWidget)


"""MONTHS_CHOICES= [
    ('-', '---'),
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
    ]"""

MONTHS_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1,13)]
MONTHS_CHOICES.insert(0,('-','---'))
YEAR_CHOICES = [(str(i), i) for i in range(2017,2031)]
YEAR_CHOICES.insert(0,('-','---'))

class FiltersForm(forms.Form):
    filtered_month= forms.CharField(label='Filter fcms on month created!', widget=forms.Select(choices=MONTHS_CHOICES))
    filtered_title = forms.CharField(label='Filter fcms which contain the word...', required=False, widget=forms.TextInput(attrs={'class': 'searchbox-input form-control'}))
    filtered_year  = forms.CharField(widget=forms.Select(choices=YEAR_CHOICES))
    #filtered_year = forms.DateField(widget=forms.SelectDateWidget(years=[number for number in range(0, 5)]))
    #filtered_year = forms.ModelChoiceField(queryset=FCM.objects.all().values('title'))
    #def __init__(self, *args, **kwargs):
        #first_year = kwargs.pop(FCM.objects.all()[0].creation_date.strftime('%Y'))
       # super(FiltersForm, self).__init__(*args, **kwargs)
      #  self.fields['filtered_year'] = [1,2,3,4,5,6,7,8]

     #   filtered_year = forms.DateField(widget=forms.SelectDateWidget(years= [number for number in range(0,5)] ))


