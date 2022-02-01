from django import forms

from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import FormActions, InlineRadios

from ..models import Municipality, Area, NewsEmail


############
# USER FORMS
############


class NewsEmailForm(forms.ModelForm):

    class Meta:
        model = NewsEmail 
        fields = ('province', 'municipality', 'areas', 'interval', 'ad_type')
        help_texts = {
            'areas': 'Håll in cmd (mac) eller ctrl (windows) för att markera flera',
            'interval': 'Hur ofta du vill få ett mail med nya annonser i valt område.',
            'ad_type': 'Vilka typer av annonser du vill bevaka.',

        }

    def __init__(self, *args, **kwargs):
        super(NewsEmailForm, self).__init__(*args, **kwargs)
        self.fields['province'].required = True
        self.fields['municipality'].required = True
        self.fields['areas'].required = False
        self.fields['interval'].required = True
        self.fields['ad_type'].required = True
        self.fields["interval"].choices = list(self.fields["interval"].choices)[1:] 
        self.fields["ad_type"].choices = list(self.fields["ad_type"].choices)[1:] 
        self.helper = FormHelper()
        if self.instance.is_active:
            button_text = 'Inaktivera'
            button_type = 'danger'
        else:
            button_text = 'Aktivera'
            button_type = 'success'

        self.helper.layout = Layout(
            Row(
                Column('province', css_class='form-group col-2 mb-0'),
                Column('municipality', css_class='form-group col-2 mb-0 ml-4'),
                Column('areas', css_class='form-group col-3 mb-0 ml-4'),
                Column(
                    InlineRadios('interval'), 
                    css_class='form-group col-1 mb-0 ml-4'
                ),
                Column(
                    InlineRadios('ad_type', css_class='p-7'), 
                    css_class='form-group col-1 mb-0 ml-4'
                ),
                Column(
                    FormActions(
                        HTML(f'<button id="cancel-subscription-button" class="btn btn-sm btn-{button_type}">{button_text}</button>'),
                        Submit('submit', 'Spara bevakning', css_class='mt-2 btn btn-sm btn-primary'),                            
                    ), 
                    css_class='form-group col-1 mt-4 mb-0 ml-4'
                ),
                
            ),
        )

        # If no province selected, clear other fields
        if not self.instance.province:
            self.fields['municipality'].queryset = Municipality.objects.none()
            self.fields['areas'].queryset = Area.objects.none()
        
        # If province selected, update municipality queryset
        if self.instance.province:
            self.fields['municipality'].queryset = Municipality.objects.filter(province_id=self.instance.province.pk).order_by('name')
        
        # If municipality selected, update area queryset
        if self.instance.municipality:
            self.fields['areas'].queryset = Area.objects.filter(municipality_id=self.instance.municipality.pk).order_by('name')


        if 'province' in self.data:
            try:
                # Set municipality queryset
                province_id = int(self.data.get('province'))
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id).order_by('name')
            
                # Set area queryset
                municipality_id = int(self.data.get('municipality'))
                self.fields['areas'].queryset = Area.objects.filter(municipality_id=municipality_id).order_by('name')
                
            except (ValueError, TypeError) as e:
                pass # invalid input from the client; ignore and fallback to empty Municipality/Area queryset

########
# ADMIN
########

class NewsEmailFormAdmin(forms.ModelForm):

    TRUE_FALSE_CHOICES = (
    (True, 'True'),
    (False, 'False')
    )

    is_active = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Is active", 
                              initial='', widget=forms.Select(), required=True)


    class Meta:
        model = NewsEmail 
        fields = ('ad_type', 'user', 'province', 'municipality', 'areas', 'interval')

    def __init__(self, *args, **kwargs):
        super(NewsEmailFormAdmin, self).__init__(*args, **kwargs)
        
        if not self.instance.province:
            self.fields['municipality'].queryset = Municipality.objects.none()
            self.fields['areas'].queryset = Area.objects.none()
        self.fields['areas'].required = False

        # If no province selected, clear other fields
        if not self.instance.province:
            self.fields['municipality'].queryset = Municipality.objects.none()
            self.fields['areas'].queryset = Area.objects.none()
        
        # If province selected, update municipality queryset
        if self.instance.province:
            self.fields['municipality'].queryset = Municipality.objects.filter(province_id=self.instance.province.pk).order_by('name')
        
        # If municipality selected, update area queryset
        if self.instance.municipality:
            self.fields['areas'].queryset = Area.objects.filter(municipality_id=self.instance.municipality.pk).order_by('name')


        if 'province' in self.data:
            try:
                # Set municipality queryset
                province_id = int(self.data.get('province'))
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id).order_by('name')
            
                # Set area queryset
                municipality_id = int(self.data.get('municipality'))
                self.fields['areas'].queryset = Area.objects.filter(municipality_id=municipality_id).order_by('name')
                
            except (ValueError, TypeError) as e:
                pass # invalid input from the client; ignore and fallback to empty Municipality/Area queryset






