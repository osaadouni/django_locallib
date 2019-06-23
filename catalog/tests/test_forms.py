import datetime

from django.test import TestCase
from django.utils import timezone


from catalog.forms import RenewBookForm, RenewBookModelForm

class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        field_label = form.fields['renewal_date'].label
        self.assertTrue(field_label == None or field_label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        help_text = form.fields['renewal_date'].help_text
        self.assertTrue(help_text, 'Enter a date between now and 4 weeks (default 3).')


    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['renewal_date'], [u"Invalid date - renewal in past"])

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['renewal_date'], [u"Invalid date - renewal more than 4 weeks ahead"])

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_is_within_the_allowed_range(self):
        date = timezone.now() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())


class RenewBookModelFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookModelForm()
        field_label = form.fields['renewal_date'].label
        self.assertTrue(field_label == None or field_label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookModelForm()
        help_text = form.fields['renewal_date'].help_text
        self.assertTrue(help_text, 'Enter a date between now and 4 weeks (default 3).')


    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookModelForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['renewal_date'], [u"Invalid date - renewal in past"])

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookModelForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['renewal_date'], [u"Invalid date - renewal more than 4 weeks ahead"])

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookModelForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_is_within_the_allowed_range(self):
        date = timezone.now() + datetime.timedelta(weeks=4)
        form = RenewBookModelForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
