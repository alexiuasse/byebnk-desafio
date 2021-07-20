from django import forms
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Field
from crispy_forms.bootstrap import PrependedText
from django.utils.translation import gettext as _

from .models import *


class AssetForm(forms.ModelForm):

    id = forms.IntegerField(initial=0)

    layout = Layout(
        Field('id', type='hidden'),
        Field('user', type='hidden'),
        Row(
            Field('name', wrapper_class="col-md-6 col-sm-12"),
            Field('modality', wrapper_class="col-lg-6 col-sm-12"),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = self.layout
        self.helper.form_class = 'form-control'

    class Meta:
        model = Asset
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name'].capitalize()
        if Asset.objects.filter(name=name).count() > 0:
            raise forms.ValidationError(_("Asset already exists!"))
        return name


class ApplianceForm(forms.ModelForm):

    id = forms.IntegerField(initial=0)

    layout = Layout(
        Field('id', type='hidden'),
        Field('user', type='hidden'),
        Field('ip_address', type='hidden'),
        Row(
            Field('asset', wrapper_class="col-md-6 col-sm-12"),
            Field('request_date', wrapper_class="col-lg-6 col-sm-12"),
        ),
        Row(
            Field('quantity', wrapper_class="col-lg-6 col-sm-12"),
            PrependedText('unit_price', settings.MONEY_SYMBOL,
                          wrapper_class="col-lg-6 col-sm-12"),
        ),

    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = self.layout
        self.helper.form_class = 'form-control'

    class Meta:
        model = Appliance
        widgets = {
            'request_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        }
        fields = '__all__'


class RedeemForm(forms.ModelForm):

    id = forms.IntegerField(initial=0)

    layout = Layout(
        Field('id', type='hidden'),
        Field('user', type='hidden'),
        Field('ip_address', type='hidden'),
        Row(
            Field('asset', wrapper_class="col-md-6 col-sm-12"),
            Field('request_date', wrapper_class="col-lg-6 col-sm-12"),
        ),
        Row(
            Field('quantity', wrapper_class="col-lg-6 col-sm-12"),
            PrependedText('unit_price', settings.MONEY_SYMBOL,
                          wrapper_class="col-lg-6 col-sm-12"),
        ),

    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = self.layout
        self.helper.form_class = 'form-control'

    class Meta:
        model = Redeem
        widgets = {
            'request_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        }
        fields = '__all__'
