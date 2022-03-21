from django import forms
from .models import UserProfile, Lecture
from django.contrib.auth.models import User


class UploadLectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = (
            'title',
            'video_url',
            'slideshow_url',
            'course',
            'professor'
        )


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('is_professor',)
