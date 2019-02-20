from django import forms
from .models import User
from course.models import Course
from assessment.models import Assessment


class UserForm(forms.ModelForm):
    username = forms.CharField(label='帳號')
    password = forms.CharField(label='密碼', widget=forms.PasswordInput())
    passwordCheak = forms.CharField(label='確認密碼', widget=forms.PasswordInput())
    email = forms.EmailField(label='電子信箱', widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'passwordCheak']

    # def clean_passwordCheak(self):
    #     password = self.cleaned_data.get('password')
    #     passwordCheak = self.cleaned_data.get('passwordCheak')
    #     if password and passwordCheak and password != passwordCheak:
    #         raise forms.ValidationError('兩次密碼不同')
    #     return passwordCheak

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(user.password)
        user.nickName = user.username
        user.course_progress = Course.objects.get(lesson=0, chapter=1)
        user.assess_progress = Assessment.objects.get(pk=12)
        if commit:
            user.save()
        return user
