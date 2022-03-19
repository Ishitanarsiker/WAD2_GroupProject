from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

# class CourseForm(forms.Form):
# 	class Meta:
#         model = Course
#         fields = ('name', 'code', 'user')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['user'].queryset = User.objects.none()
#
#         if 'name' in self.data:
#             try:
#                 country_id = int(self.data.get('name'))
#                 self.fields['user'].queryset = User.objects.filter(name_id=name_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty City queryset
#         elif self.instance.pk:
#             self.fields['user'].queryset = self.instance.country.user_set.order_by('name')
#


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('is_professor',)
