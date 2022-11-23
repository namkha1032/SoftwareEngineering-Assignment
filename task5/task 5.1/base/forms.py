from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User, MCP_Collector, Calendar
from django.contrib.admin.widgets import AdminDateWidget
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [ 'username']


class DateForm(ModelForm):
    class Meta:
        model = Calendar
        fields = '__all__'
        widgets = {'date': DateInput()}
