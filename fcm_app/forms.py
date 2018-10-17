from django import forms
from ckeditor.widgets import CKEditorWidget
from django_countries.widgets import CountrySelectWidget
from django_countries import countries
import calendar
from .models import FCM

class MyMultipleChoiceField(forms.MultipleChoiceField):
    def validate(self, value):
        return True

STATUS_CHOICES= [
    ('1', 'Public'),
    ('2', 'Private'),
    ]

class FCMForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'cols': '50'}))
    tags = MyMultipleChoiceField(label='Tags', required=False,
                                 widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
                                 choices=())
    country = forms.ChoiceField(label = 'Country', initial = 'GR', widget = CountrySelectWidget(attrs={'class': 'form-control'}), choices=countries)
    status = forms.IntegerField(label='Status', initial = 1, widget= forms.RadioSelect(choices = STATUS_CHOICES))
    map_image = forms.FileField(label='Image', widget=forms.FileInput(attrs={'class': 'form-control'}))
    map_html = forms.FileField(label='HTML', widget=forms.FileInput(attrs={'class': 'form-control'}))


class FCMCONCEPTForm(forms.Form):
    concept_info = forms.CharField(widget=CKEditorWidget)


class FCMEDGEForm(forms.Form):
    edge_info = forms.CharField(widget=CKEditorWidget)


def first_year():
    return int(FCM.objects.all().order_by('creation_date')[0].creation_date.strftime('%Y'))


def last_year():
    import datetime
    now = datetime.datetime.now()
    return now.year

def selected_years():
    x = FCM.objects.all()
    YEAR_CHOICES = []
    if x!=0:
        # YEAR_CHOICES = [(str(i), i) for i in range(first_year(), last_year() + 1)]
        YEAR_CHOICES = [(str(i.year),i.year) for i in FCM.objects.all().datetimes('creation_date', 'year')]
    YEAR_CHOICES.insert(0, ('-', '---'))
    return YEAR_CHOICES

MONTHS_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1,13)]
MONTHS_CHOICES.insert(0,('-','---'))

# COUNTRIES_CHOICES = [(countries[i][0], countries[i][1]) for i in range(0,len(countries))]
# COUNTRIES_CHOICES.insert(0,('-','---'))

SORT_CHOICES = [
    ('creation_date', 'Creation date'),
    ('title', 'Title'),
    ]

SORT_ORDERS = [
    ('ascending ', 'ASC '),
    ('descending', 'DESC'),
    ]


def selected_countries():
    x = FCM.objects.all().distinct('country')
    if x!=0:
        my = x.values('country')
        my_countries_codes = []
        for index in range(len(my)):
            for key in my[index]:
                my_countries_codes.append(my[index][key])
        oles = [(countries[i][0], countries[i][1]) for i in range(0,len(countries))]
        final_countries = []
        for m in my_countries_codes:
            final_countries.append([item for item in oles if item[0] == m])
        flat_list = [item for sublist in final_countries for item in sublist]
    flat_list.insert(0, ('-', '---'))
    return flat_list


class FiltersForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # super(self.__class__, self).__init__(*args, **kwargs)
        super(FiltersForm, self).__init__(*args, **kwargs)
        self.fields['filtered_year'].choices = selected_years()
        self.fields['filtered_country'].choices = selected_countries()

    filtered_title_and_or_description = forms.CharField(label='Filter fcms which contain the word...', required=False, widget=forms.TextInput(attrs={'class': 'searchbox-input form-control'}))
    filtered_tags = MyMultipleChoiceField(label='Filter fcms which contain one of the tags...', required=False,
                                              widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
                                              choices=())
    filtered_getmine = forms.BooleanField(required=False)
    filtered_year = forms.ChoiceField(widget=forms.Select(choices=[]))
    filtered_country = forms.ChoiceField(widget=forms.Select(choices=[]))
    filtered_sorting_type = forms.CharField(label='Order by:', widget=forms.Select(choices=SORT_CHOICES))
    filtered_sorting_order = forms.CharField(widget=forms.Select(choices=SORT_ORDERS))



class jsForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'cols': '50'}))
    tags = MyMultipleChoiceField(label='Tags', required=False,
                                 widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
                                 choices=())
    status = forms.IntegerField(label='Status', initial=1, widget=forms.RadioSelect(choices=STATUS_CHOICES))
    country = forms.ChoiceField(label = 'Country', initial = 'GR', widget = CountrySelectWidget(attrs={'class': 'form-control'}), choices=countries)
    chartis = forms.CharField(label='Chartis',widget=forms.HiddenInput())
    image = forms.CharField(label='Image',widget=forms.HiddenInput())


class SortMapsForm(forms.Form):
    sorting_type = forms.CharField(label='Order by:', widget=forms.Select(choices=SORT_CHOICES))
