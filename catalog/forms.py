import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from bootstrap_datepicker_plus import DatePickerInput

from .models import BookInstance, Book


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).",
                                   widget=DatePickerInput(format="%Y-%m-%d")
                                   )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']


        # Check if a date is not in the past.
        if data < datetime.date.today():
            print('Invalid date - renewal in pase')
            raise ValidationError(_('Invalid date - renewal in pase'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            print('Invalid date - renewal more than weeks ahead')
            raise ValidationError(_('Invalid date - renewal more than weeks ahead'))

        # Remember to always return the cleaned data.
        return data


class RenewBookModelForm(forms.ModelForm):

    due_back = forms.DateField(widget=DatePickerInput(format="%Y-%m-%d"))

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        # Check if a date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the alloweed range (+4 weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data
        return data


    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('New renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}



class BookModelForm(forms.ModelForm):

    class Meta:
        model = Book
        #fields = '__all__'
        fields = ['title', 'summary', 'isbn', 'genre', 'language']


class BookInstanceModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].initial = 'a'
        self.fields['id'].widget.attrs['readonly'] = True

    class Meta:
        model = BookInstance
        fields = ('id', 'imprint', 'status')
        #fields = '__all__'
