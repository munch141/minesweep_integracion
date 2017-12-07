from django import forms
from builder.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate

# class GenericForm(forms.ModelForm):
# 	class Meta:
# 		model = Generic
# 		exclude = ()

# class AskForm(forms.ModelForm):
# 	class Meta:
# 		model = Pregunta
# 		fields = ('ask',)

class registerForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username','password1','password2')

	def __init__(self, *args, **kwargs):
		super(registerForm, self).__init__(*args, **kwargs)

		for key in self.fields:
			self.fields[key].widget.attrs['class'] = 'form-control'
			self.fields[key].widget.attrs['required'] = True
			self.fields[key].widget.attrs['id'] = 'id_'+key
			self.fields[key].widget.attrs['placeholder'] = self.fields[key].label

class loginForm(forms.Form):

	username = forms.CharField(max_length= 150,widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control','required':'True'}))
	password = forms.CharField(max_length = 20, widget=forms.PasswordInput(attrs={'placeholder':'Password','type':'password','class':'form-control','required':'True'}))
	def __init__(self, *args, **kwargs):
		super(loginForm, self).__init__(*args, **kwargs)

	def clean_password(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError("Los datos ingresados son inválidos.")
		
		return password