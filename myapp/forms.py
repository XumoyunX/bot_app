from django import forms
from myapp.models import User
class UsersForm(forms.ModelForm):
    class Meta:
        model = User()
        fields = '__all__'
