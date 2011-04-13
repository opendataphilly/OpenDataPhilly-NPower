from django import forms
from models import UpdateFrequency, CoordSystem, UrlType, DataType

class SuggestionForm(forms.Form):
    dataset_name = forms.CharField(max_length=255)
    organization = forms.CharField(max_length=255)
    contact_email = forms.CharField(max_length=255)
    contact_phone = forms.CharField(max_length=255)
    url = forms.CharField(max_length=255)
    time_period = forms.CharField(max_length=255)
    release_date = forms.DateField()
    copyright_holder = forms.CharField(max_length=255)
    area_of_interest = forms.CharField(max_length=255)
    
    update_frequency = forms.ModelChoiceField(queryset=UpdateFrequency.objects.all())
    coord_system = forms.ModelChoiceField(queryset=CoordSystem.objects.all())
    type = forms.ModelChoiceField(queryset=UrlType.objects.all())
    formats = forms.ModelMultipleChoiceField(queryset=DataType.objects.all())
    
    usage_limitations = forms.CharField(max_length=1000, widget=forms.Textarea)
    collection_process = forms.CharField(max_length=1000, widget=forms.Textarea)
    data_purpose = forms.CharField(max_length=1000, widget=forms.Textarea)
    intended_audience = forms.CharField(max_length=1000, widget=forms.Textarea)
    why = forms.CharField(max_length=1000, widget=forms.Textarea)
    certified = forms.BooleanField()
    
    