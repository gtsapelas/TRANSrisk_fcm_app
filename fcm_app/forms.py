from django import forms
from ckeditor.widgets import CKEditorWidget


class FCMForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'cols': '50'}))
    map_image = forms.FileField(label='Image', widget=forms.FileInput())
    map_html = forms.FileField(label='HTML', widget=forms.FileInput)


class FCMCONCEPTForm(forms.Form):
    concept_info = forms.CharField(widget=CKEditorWidget)


MONTHS_CHOICES= [
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
    ]

class MonthsForm(forms.Form):
    filtered_month= forms.CharField(label='Filter fcms on month created!', widget=forms.Select(choices=MONTHS_CHOICES))
