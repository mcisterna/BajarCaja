# -*- coding: utf-8 -*-

from django import forms
from datetime import datetime
from models import CN, Type_Fact, Type_Coin
from django.utils.encoding import smart_str

class FacturaForm(forms.Form):
	
	upload_file = forms.FileField()			
	monto = forms.IntegerField(widget=forms.TextInput(attrs={'class':'monto_factura', 'placeholder':'Monto'}), label='* Monto')
	coin = forms.ChoiceField(label='* Tipo Moneda', widget=forms.Select(attrs={'class':'select_chico'}))
	glosa = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'glosa_factura', 'placeholder':'Glosa'}), label='* Glosa')
	iva = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'iva'}))
	orden_compra = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'orden_compra'}))
	checkboxCoin = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'checkboxCoin'}))
	checkboxMonto = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'checkboxMonto'}))
	checkboxGlosa = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'checkboxGlosa'}))
	fecha_fact_plan = forms.CharField(
									max_length=100,
									widget=forms.TextInput(attrs={'class':'fecha_fact_plan', 'placeholder':'Click para agregar fecha','readonly':'true'}),
									label='* Fecha Facturación'
					)
	fecha_fact_real = forms.CharField(
									max_length=100,
									widget=forms.TextInput(attrs={'class':'fecha_fact_real', 'placeholder':'Click para agregar fecha'}),
									label='* Fecha Real Facturación',
									required=False
					)
	fecha_pago_plan = forms.CharField(
									max_length=100,
									widget=forms.TextInput(attrs={'class':'fecha_pago_plan', 'placeholder':'Click para agregar fecha'}),
									label='* Fecha Pago',
									required=False
					)
	fecha_pago_real = forms.CharField(
									max_length=100,
									widget=forms.TextInput(attrs={'class':'fecha_pago_real', 'placeholder':'Click para agregar fecha'}),
									label='* Fecha Real Pago',
									required=False
					)
	
	def clean_coin(self):
		coin = self.cleaned_data.get('coin')
		if coin == '0':
			raise forms.ValidationError("Debe seleccionar un tipo de moneda.")
		return coin

	def daysofmonth(self,month,year):
		if month == 4 or month == 6 or month == 9 or month == 11:
			return 30
		elif month == 2:
			return self.bisiesto(year)
		else:
			return 31

	def bisiesto(self,year):
		if (year%4 == 0 and year%100 != 0) or year%400 == 0:
			return 29
		else:
			return 28

	def clean_fecha_fact_plan(self):
		ffp = self.cleaned_data.get('fecha_fact_plan')
		numdates = str(ffp).split("-")
		if len(numdates) != 3:
			raise forms.ValidationError("Debe ingresar una fecha válida.")
		curr_year = datetime.now().year
		try:
			year = int(numdates[0])
			month = int(numdates[1])
			day = int(numdates[2])
			dom = self.daysofmonth(month,year)
			if year >= curr_year and (month >= 1 and month <= 12) and (day >= 1 and day <= dom):
				return ffp
			else:
				raise forms.ValidationError("Debe ingresar una fecha válida.")
		except ValueError:
			raise forms.ValidationError("Debe ingresar una fecha válida.")

	def clean_fecha_fact_real(self):
		ffr = self.cleaned_data.get('fecha_fact_real')
		ffp = self.cleaned_data.get('fecha_fact_plan')
		if str(ffr) == '':
			return ffr
		if ffr < ffp:
			raise forms.ValidationError("La fecha de facturación real no puede ser antes que la fecha de facturación planificada.")
		numdates = str(ffr).split("-")
		if len(numdates) != 3:
			raise forms.ValidationError("Debe ingresar una fecha válida.")
		curr_year = datetime.now().year
		try:
			year = int(numdates[0])
			month = int(numdates[1])
			day = int(numdates[2])
			dom = self.daysofmonth(month,year)
			if year >= curr_year and (month >= 1 and month <= 12) and (day >= 1 and day <= dom):
				return ffr
			else:
				raise forms.ValidationError("Debe ingresar una fecha válida.")
		except ValueError:
			raise forms.ValidationError("Debe ingresar una fecha válida.")

	def clean_fecha_pago_plan(self):
		fpp = self.cleaned_data.get('fecha_pago_plan')
		if str(fpp) == '':
			return fpp
		numdates = str(fpp).split("-")
		if len(numdates) != 3:
			raise forms.ValidationError("Debe ingresar una fecha válida.")
		curr_year = datetime.now().year
		try:
			year = int(numdates[0])
			month = int(numdates[1])
			day = int(numdates[2])
			dom = self.daysofmonth(month,year)
			if year >= curr_year and (month >= 1 and month <= 12) and (day >= 1 and day <= dom):
				return fpp
			else:
				raise forms.ValidationError("Debe ingresar una fecha válida.")
		except ValueError:
			raise forms.ValidationError("Debe ingresar una fecha válida.")

	def clean_fecha_pago_real(self):
		fpr = self.cleaned_data.get('fecha_pago_real')
		if str(fpr) == '':
			return fpr
		numdates = str(fpr).split("-")
		if len(numdates) != 3:
			raise forms.ValidationError("Debe ingresar una fecha válida.")
		curr_year = datetime.now().year
		try:
			year = int(numdates[0])
			month = int(numdates[1])
			day = int(numdates[2])
			dom = self.daysofmonth(month,year)
			if year >= curr_year and (month >= 1 and month <= 12) and (day >= 1 and day <= dom):
				return fpr
			else:
				raise forms.ValidationError("Debe ingresar una fecha válida.")
		except ValueError:
			raise forms.ValidationError("Debe ingresar una fecha válida.")
			

	def __init__(self, *args, **kwargs):
		super(FacturaForm, self).__init__(*args, **kwargs)
		self.fields['coin'].choices = [(0,'Seleccione... ')]+[(b.id, smart_str(b.__unicode__()).title()) for b in Type_Coin.objects.all()]



class ProyectoForm(forms.Form):

	nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'', 'placeholder':'Nombre del Proyecto'}), label='* Nombre del Proyecto')
	cn = forms.ChoiceField(label='* CN', widget=forms.Select(attrs={'class':'select_chico'}))
	type_fact = forms.ChoiceField(label='* Tipo Factura', widget=forms.Select(attrs={'class':'select_chico'}))
	num_fact = forms.IntegerField(widget=forms.TextInput(attrs={'class':'', 'placeholder':'N° Facturas'}), label='* N° Facturas')
	responsable = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'', 'placeholder':'Responsable'}), label='* Responsable')
	cliente = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'', 'placeholder':'Cliente'}), label='* Cliente')

	def clean_cn(self):
		cn = self.cleaned_data.get('cn')
		if cn == '0':
			raise forms.ValidationError("Debe seleccionar un Centro de Negocios.")
		return cn

	def clean_type_fact(self):
		tf = self.cleaned_data.get('type_fact')
		if tf == '0':
			raise forms.ValidationError("Debe seleccionar un tipo de factura.")
		return tf

	def __init__(self, *args, **kwargs):
		super(ProyectoForm, self).__init__(*args, **kwargs)
		self.fields['cn'].choices = [(0,'Seleccione... ')]+[(b.id, smart_str(b.name).title()) for b in CN.objects.all()]
		self.fields['type_fact'].choices = [(0,'Seleccione... ')]+[(b.id, smart_str(b.type).title()) for b in Type_Fact.objects.all()]

