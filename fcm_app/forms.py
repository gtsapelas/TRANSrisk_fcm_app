from django import forms
from ckeditor.widgets import CKEditorWidget


class FCMForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'cols': '50'}))
    map_image = forms.FileField(label='Image', widget=forms.FileInput())
    map_html = forms.FileField(label='HTML', widget=forms.FileInput)


class FCMCONCEPTForm(forms.Form):
    concept_info = forms.CharField(widget=CKEditorWidget)


class jsForm(forms.Form):
    #description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'cols': '50'}))
    title = forms.CharField(label='Title', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', max_length=10000)