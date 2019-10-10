import pytest

from werkzeug.datastructures import MultiDict

from server.forms.form import BaseForm
from server.forms.fields import *


class DummyForm(BaseForm):
    field1 = IntegerField('int', min=0, max=10, default=1)
    field2 = IntegerField('m_int', multiple=True, required=False)
    field3 = IntegerField('m_int2', multiple=True, required=False)
    field4 = IntegerField('m_int3', multiple=True, required=False)
    field5 = DecimalField('float', min=0.0, max=10.0, required=False)
    field6 = TextField('text', required=False)
    field7 = BooleanField('bool')
    field8 = BooleanField('bool2', required=False)
    CHOICES = [('a', 'A'), ('b', 'B'), ('c', 'C')]
    field9 = ChoiceField('choice', choices=CHOICES)
    field10 = ChoiceField('m_choice', choices=CHOICES, multiple=True)


@pytest.fixture()
def valid_form():
    form = DummyForm(MultiDict([
        ('int', '5'),
        ('m_int', '10'), ('m_int', '15'), ('m_int', '0'),
        ('m_int2', '2'),
        ('float', '5.0'),
        ('text', 'foo bar baz'),
        ('bool', 'yes'),
        ('bool2', 'no'),
        ('choice', 'a'),
        ('m_choice', 'a'),
        ('m_choice', 'c')
    ]))
    assert form.is_valid()
    return form


def test_cleaned_integer_field(valid_form):
    assert valid_form.cleaned_data['int'] == 5


def test_cleaned_multiple(valid_form):
    assert valid_form.cleaned_data['m_int'] == [10, 15, 0]


def test_cleaned_multiple_one_value(valid_form):
    assert valid_form.cleaned_data['m_int2'] == [2]


def test_cleaned_multiple_no_value(valid_form):
    assert valid_form.cleaned_data['m_int3'] == []


def test_cleaned_decimal_field(valid_form):
    assert valid_form.cleaned_data['float'] == 5.0


def test_cleaned_text_field(valid_form):
    assert valid_form.cleaned_data['text'] == 'foo bar baz'


def test_cleaned_bool_true_value(valid_form):
    assert valid_form.cleaned_data['bool'] is True


def test_cleaned_bool_false_value(valid_form):
    assert valid_form.cleaned_data['bool2'] is None


def test_cleaned_choice_field(valid_form):
    assert valid_form.cleaned_data['choice'] == 'a'


def test_cleaned_multiple_choice_field(valid_form):
    assert valid_form.cleaned_data['m_choice'] == ['a', 'c']
