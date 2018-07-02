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
    map_image = forms.FileField(label='Image', widget=forms.FileInput(attrs={'class': 'form-control'}))
    map_html = forms.FileField(label='HTML', widget=forms.FileInput(attrs={'class': 'form-control'}))

class FCMCONCEPTForm(forms.Form):
    concept_info = forms.CharField(widget=CKEditorWidget)


def first_year():
    # return 2017
    return int(FCM.objects.all().order_by('creation_date')[0].creation_date.strftime('%Y'))

def last_year():
    import datetime
    now = datetime.datetime.now()
    return now.year

MONTHS_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1,13)]
MONTHS_CHOICES.insert(0,('-','---'))

YEAR_CHOICES = [(str(i), i) for i in range(first_year(),last_year()+1)]
YEAR_CHOICES.insert(0,('-','---'))

COUNTRIES_CHOICES = [(countries[i][0], countries[i][1]) for i in range(0,len(countries))]
COUNTRIES_CHOICES.insert(0,('-','---'))

class FiltersForm(forms.Form):
    filtered_title = forms.CharField(label='Filter fcms which contain the word...', required=False, widget=forms.TextInput(attrs={'class': 'searchbox-input form-control'}))
    filtered_year = forms.CharField(widget=forms.Select(choices=YEAR_CHOICES))
    filtered_country = forms.CharField(widget=forms.Select(choices=COUNTRIES_CHOICES))




class jsForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    # description = forms.CharField(label='Description', max_length=10000)
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'cols': '50'}))
    status = forms.IntegerField(label='Status', initial=1, widget=forms.RadioSelect(choices=STATUS_CHOICES))
    country = forms.ChoiceField(label = 'Country', widget = CountrySelectWidget(attrs={'class': 'form-control'}), choices=countries)
    chartis = forms.CharField(label='Chartis',widget=forms.HiddenInput())
