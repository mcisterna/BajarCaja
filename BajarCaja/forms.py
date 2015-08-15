# -*- coding: utf-8 -*-

from django import forms

class UploadForm(forms.Form):
	upload_file = forms.FileField()
	choices = forms.ChoiceField(choices=[('publico','Público'),('privado','Privado')], widget=forms.RadioSelect())

class RegisterForm(forms.Form):
	username = forms.CharField(
		label="Nombre de Usuario",
		max_length=32,
		required=True,
		widget=forms.TextInput(attrs={'autocomplete':'off'}))
	password = forms.CharField(
		label="Contraseña",
		min_length=5,
		max_length=32,
		widget=forms.PasswordInput(attrs={'autocomplete':'off'}),
		required=True)
	password_confirmation = forms.CharField(
		label="Confirmar Contraseña",
		widget=forms.PasswordInput(attrs={'autocomplete':'off'}),
		min_length=5,
		max_length=32,
		required=True)
	email = forms.EmailField(label="Email", max_length=128, required=False,widget=forms.EmailInput(attrs={'autocomplete':'off'}))
	first_name = forms.CharField(
		label="Nombre",
		max_length=128,
		required=False,
		widget=forms.TextInput(attrs={'autocomplete':'off'}))
	last_name = forms.CharField(label="Apellido",
		max_length=128,
		required=False,
		widget=forms.TextInput(attrs={'autocomplete':'off'}))

	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()
		if (cleaned_data.get('password') !=
				cleaned_data.get('password_confirmation')):
			raise forms.ValidationError('Las contraseña no calzan.')
