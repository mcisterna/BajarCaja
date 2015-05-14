# -*- coding: utf-8 -*-

from django import forms

class UploadForm(forms.Form):
	upload_file = forms.FileField()
	choices = forms.ChoiceField(choices=[('publico','Público'),('privado','Privado')], widget=forms.RadioSelect())