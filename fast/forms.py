from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import Group

class FileUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        if not (uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.xlsx')):
            raise forms.ValidationError("Only .csv or .xlsx files are supported.")
        return uploaded_file
    # Form for creating a user with role selection
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('supervisor', 'Supervisor'), ('analyst', 'Analyst'), ('viewer', 'Viewer')], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        # Assign role to the user
        role = self.cleaned_data['role']
        group, created = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        return user


# Form for updating user details (email, active status, and role)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    is_active = forms.BooleanField(required=False)
    role = forms.ChoiceField(choices=[('supervisor', 'Supervisor'), ('analyst', 'Analyst'), ('viewer', 'Viewer')], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        # Update the role
        role = self.cleaned_data['role']
        group, created = Group.objects.get_or_create(name=role)
        user.groups.clear()  # Remove existing roles
        user.groups.add(group)

        return user


# Form to handle user blocking (deactivating the account)
class BlockUserForm(forms.Form):
    user_id = forms.IntegerField()

    def clean_user_id(self):
        user_id = self.cleaned_data['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise forms.ValidationError("User does not exist.")
        return user
