from .models import MyUser
from django import forms


class MyUserCreationForm(forms.ModelForm):
	"""
	A form for creating users.  Forces a repeated password
	"""
	password1 = forms.CharField(
		label='Password',
		widget=forms.PasswordInput
	)
	password2 = forms.CharField(
		label='Password confirmation',
		widget=forms.PasswordInput
	)

	class Meta:
		model = MyUser
		fields = (
			'email',
			'first_name',
			'last_name',
			'password1',
			'password2',
		)

	def clean_password2(self):
		# make sure password entries match
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(MyUserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class MyUserChangeForm(forms.ModelForm):
	"""
	a form for updating user details.  this does NOT allow a password change
	"""

	class Meta:
		model = MyUser
		fields = (
			'email',
			'first_name',
			'last_name',
		)
	def clean_password(self):
		return self.initial['password']