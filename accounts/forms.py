from django import forms
from .models import User,OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    password=forms.CharField(label='password',widget=forms.PasswordInput)
    password2=forms.CharField(label='confirm password ',widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=('email','phone_number','full_name')
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password'] and cd['password2'] and cd['password'] != cd['password2']:
            raise ValidationError('پسورد ها یکسان نیستند')
        return cd['password2'] 

    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user  

class UserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField(help_text="you cant change password using <a href=\"../password/\">this form</a>.")
    class Meta:
        model=User
        fields=('email','phone_number','full_name','password','last_login')

    
class UserRegistrationForm(forms.Form):
    email=forms.EmailField(label='',widget=forms.EmailInput(attrs={'class': 'form-row input-text','placeholder':'ایمیل'}) )
    full_name=forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-row input-text','placeholder':'نام'}))    
    phone=forms.CharField(label='',max_length=11,widget=forms.TextInput(attrs={'class': 'form-row input-text','placeholder':'تلفن همراه'}))
    password=forms.CharField(label='',widget=forms.PasswordInput(attrs={'class': 'form-row input-text','placeholder':'گذرواژه'}))
    password2=forms.CharField(label='',widget=forms.PasswordInput(attrs={'class': 'form-row input-text','placeholder':'تایید گذرواژه'}))
    
    
    def clean(self):
        cd=super().clean()
        p1=cd.get('password')
        p2=cd.get('password2')
        if p1 and p2 and p1!=p2:
                        raise ValidationError('گذرواژه ها  یکسان نیستند')
    def clean_email(self):
        email=self.cleaned_data['email']
        user=User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('این ایمیل قبلا انتخاب شده است')
        return email    

    def clean_phone(self):
        phone=self.cleaned_data['phone']
        user=User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('این شماره  قبلا انتخاب شده است')
        OtpCode.objects.filter(phone_number=phone).delete() 
        return phone 

class VerifyCodeForm(forms.Form):
    code=forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class': 'form-row input-text','placeholder':'کد'}) )



class UserLoginForm(forms.Form):
    phone=forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-row input-text','placeholder':'تلفن همراه'}))    

    password=forms.CharField(label='',widget=forms.PasswordInput(attrs={'class': 'form-row input-text','placeholder':'گذرواژه'}))
