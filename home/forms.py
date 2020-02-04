from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Member, FileModel, Contest, Submission
import datetime
from django.contrib.auth import authenticate, login

class MemberCreationForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ('username', 'email')


class MemberChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = ('username', 'email')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class ModelFormWithFileField(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ['file_name', 'file', 'datetime']
        widgets = {
            'datetime': forms.DateTimeInput(),
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('file', )

class MemberCreationUIForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Member
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        try:
            mem = Member.objects.filter(username=username)
        except:
            mem = None
        if mem:
            raise forms.ValidationError("Username has been existed!")
        if password1 != password2:
            raise forms.ValidationError("Passwords is not similar!")
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Wrong username or password. Please try again!!")

        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


    



        