import datetime
import string

from django import forms
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from . import models


class AvatarUpload(forms.ModelForm):
    class Meta:
        model = models.User
        fields = [
            'avatar',
        ]


class EditSignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = [
            'bio',
            'birth_date',
            'city',
            'state',
            'country',
            'animal',
            'hobby',
        ]
        exclude = [
            'password1',
            'password2',
        ]

    def clean(self):
        cleaned_data = super().clean()
        bio = cleaned_data.get('bio')
        birth_date = cleaned_data.get('birth_date')

        msg_bio = "Bio must be longer then 15 characters!"

        if len(bio) < 10:
            self.add_error('bio', msg_bio)

        try:
            print(type(birth_date))
            datetime.datetime.strptime(str(birth_date), "%Y-%m-%d")
        except ValueError:
            self.add_error('birth_date', "Incorrect date")

        return cleaned_data



class SignUpForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'bio',
        ]


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        bio = cleaned_data.get('bio')

        # error messages
        msg_username = "Username already exists!"
        msg_short_password = "Password must be longer than 15 characters!"
        msg_weak_password = "Password cannot contain username, last_name or first_name"
        msg_weak_password_lowercase = ('Password must contain both upper and'
        ' lowercase and must include one or more numerical digits!')
        msg_bio = "Bio must be longer then 15 characters!"

        # username check
        try:
            match = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            pass
        else:
            self.add_error('username', msg_username)

        # password length check
        if len(password1) < 15:
            self.add_error('password1', msg_short_password)

        # Password must contain an lowercase letter
        # Password must contain an uppercase letter
        # Password must contain a digit
        # Password must contain a special character
        if (
        not len(set(string.ascii_lowercase).intersection(password1))
        or not len(set(string.ascii_uppercase).intersection(password1))
        or not len(set(string.digits).intersection(password1))
        or not len(set(string.punctuation).intersection(password1))
        ):
            self.add_error('password1', msg_weak_password_lowercase)

        if password1 in username:
            self.add_error('password1', msg_weak_password)

        if password1 in first_name:
            self.add_error('password1', msg_weak_password)

        if password1 in last_name:
            self.add_error('password1', msg_weak_password)

        if len(bio) < 10:
            self.add_error('bio', msg_bio)

        return cleaned_data
