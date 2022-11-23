from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, MCP_Collector, Calendar
from django.contrib.admin.widgets import AdminDateWidget
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class DateForm(ModelForm):
    class Meta:
        model = Calendar
        fields = '__all__'
        widgets = {'date': DateInput()}
