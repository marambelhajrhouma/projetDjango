from django import forms
from django.contrib.auth.hashers import make_password
from django.forms import PasswordInput  
from .models import Employee, EmployeeProfile

#_________________________ RegistrationForms
class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=PasswordInput, label='Password')
    password2 = forms.CharField(widget=PasswordInput, label='Confirm Password')

    class Meta:
        model = Employee
        fields = ['name', 'department', 'position', 'email', 'password1', 'password2', 'phone_number']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user

#_________________________ LoginForms
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

#__________________________ 
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'department', 'position', 'email', 'phone_number']

#_________________________ UpdateEmployee
class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'department', 'position', 'email', 'phone_number']

#_________________________ EmployeeProfileForm
class EmployeeProfileForm(forms.ModelForm):
    # Include fields from the Employee model
    email = forms.EmailField(disabled=True)
    name = forms.CharField(disabled=True)
    position = forms.ModelChoiceField(queryset=Employee.objects.all(), disabled=True)
    department = forms.ModelChoiceField(queryset=Employee.objects.all(), disabled=True)
    phone_number = forms.CharField(disabled=True)
    joined_date = forms.DateField(disabled=True)
    birth_date = forms.DateField()
    gender = forms.ChoiceField(choices=Employee.gender_choices)
    age = forms.IntegerField()

    class Meta:
        model = EmployeeProfile
        fields = ['skills', 'qualifications']

    def __init__(self, *args, **kwargs):
        # Retrieve the user instance from the keyword arguments
        user_instance = kwargs.pop('user_instance', None)

        super().__init__(*args, **kwargs)

        # Set initial values from the provided user instance
        if user_instance:
            self.initial['email'] = user_instance.email
            self.initial['name'] = user_instance.name
            self.initial['position'] = user_instance.position
            self.initial['department'] = user_instance.department
            self.initial['phone_number'] = user_instance.phone_number
            self.initial['joined_date'] = user_instance.joined_date