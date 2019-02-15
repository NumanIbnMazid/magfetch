from django import forms
from .models import Date
import datetime

# class DateInput(forms.DateInput):
#     input_type = 'date'

class DateCreateForm(forms.ModelForm):
    academic_year_fake = forms.CharField()
    def __init__(self, *args, **kwargs):
        super(DateCreateForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].help_text         = "From when students will be able to upload their contributions"
        self.fields['closure_date'].help_text       = "From when uploading new contributions will be disabled"
        self.fields['final_closure_date'].help_text = "From when modification of contributions will be disabled"
        self.fields['status'].help_text             = "Contribution collection will be functional if Publication Status is Published"
        today       = datetime.date.today()
        next_year   = datetime.datetime(year=today.year+1, month=1, day=1)
        self.initial['academic_year_fake']          = "%s-%s" %(today.strftime("%Y"), next_year.strftime("%Y")[-2:])
        self.fields['academic_year_fake'].widget.attrs['readonly'] = True
        self.fields['academic_year_fake'].required  = False
        self.fields['academic_year_fake'].label     = "Academic Year"
        self.fields['status'].label                 = "Publication Status"
        self.fields['start_date'].widget.attrs.update({
            'id': 'datetimepicker1',
            'autocomplete': 'off'
        })
        self.fields['closure_date'].widget.attrs.update({
            'id': 'datetimepicker2',
            'autocomplete': 'off'
        })
        self.fields['final_closure_date'].widget.attrs.update({
            'id': 'datetimepicker3',
            'autocomplete': 'off'
        })

    class Meta:
        model   = Date
        fields  = ['start_date', 'closure_date', 'final_closure_date', 'status']
        exclude = ['academic_year', 'slug']
        # widgets = {
        #     'start_date': DateInput(),
        #     'closure_date': DateInput(),
        #     'final_closure_date': DateInput(),
        # }

    def clean_start_date(self):
        start_date  = self.cleaned_data.get('start_date')
        if not start_date == None :
            today       = datetime.datetime.now()
            if not start_date.year == today.year:
                raise forms.ValidationError('Start Date must be within this year!')
            if start_date < today:
                raise forms.ValidationError('You cannot select previous date as Start Date!')
            return start_date
        return None

    def clean_closure_date(self):
        start_date      = self.cleaned_data.get('start_date')
        closure_date    = self.cleaned_data.get('closure_date')
        if not closure_date == None :
            today           = datetime.datetime.now()
            if not closure_date.year == today.year:
                raise forms.ValidationError('Closure Date must be within this year!')
            return closure_date
        return None

    def clean_final_closure_date(self):
        closure_date        = self.cleaned_data.get('closure_date')
        final_closure_date  = self.cleaned_data.get('final_closure_date')
        if not final_closure_date == None :
            today       = datetime.datetime.now()
            if not final_closure_date.year == today.year:
                raise forms.ValidationError('Final Closure Date must be within this year!')
            return final_closure_date
        return None
