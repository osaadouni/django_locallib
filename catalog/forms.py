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

        # Check if a date is in the past - before today - and raise an error.
        if data < datetime.date.today():
            print('Invalid date - renewal in pase')
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is too far in the future beyond the range of
        # the allowed range (more than 4 weeks from today) and raise an error
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            print('Invalid date - renewal more than 4 weeks ahead')
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Date is now OK. Remember to always return the cleaned data.
        return data


class RenewBookModelForm(forms.ModelForm):

    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).",
                               widget=DatePickerInput(format="%Y-%m-%d"))

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        today = datetime.date.today()

        #print(f"renewal_date:{data},  today: {today}")

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
        fields = ['renewal_date']
        labels = {'renewal_date': _('New renewal date')}
        help_texts = {'renewal_date': _('Enter a date between now and 4 weeks (default 3).')}



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


class BorrowBookInstanceModelForm(forms.ModelForm):

    isbn = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['status'].initial = 'a'
        #print(f"fields: {self.fields}")
        self.fields['id'].widget.attrs['readonly'] = True
        self.fields['due_back'].widget.attrs['readonly'] = True
        self.fields['isbn'].widget.attrs['readonly'] = True

    class Meta:
        model = BookInstance
        fields = ('book', 'isbn', 'id', 'due_back')
        #fields = '__all__'
