# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse, Http404
from BajarCaja.models import File
from forms import UploadForm, RegisterForm
from django.conf import settings
from datetime import datetime
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import mimetypes,os

def home(request):
	return render(request,'home.html',{})

@login_required
def show_files(request):
	latest_files = File.objects.order_by('-upload_date')
	context ={'latest_files': latest_files,}
	return render(request,'show_files.html',context)

@login_required
def upload_file(request):
	msg = ''
	if request.method == 'POST':
		form = UploadForm(request.POST,request.FILES)
		if form.is_valid():
			form = form.cleaned_data
			the_file = form['upload_file']
			user_name = 'user'
			size = the_file.size
			scale = 'B'
			if size > 1048576: # mayor a 1 MB
				size = size / 1048576.0
				scale = 'MB'
			elif size > 1024: # mayor a 1 KB
				size = size / 1024.0
				scale = 'KB'
			filepath = os.path.join(settings.BASE_DIR,'BajarCaja','uploads',user_name+'_files',the_file.name)
			if not os.path.exists(os.path.dirname(filepath)):
				os.makedirs(os.path.dirname(filepath))
			with open(filepath, 'wb') as destination:
				for chunk in the_file.chunks():
					destination.write(chunk)
			file_db = File(
						filename=the_file.name,
						upload_date=datetime.now(),
						filepath=filepath,
						size=size,
						real_size=the_file.size,
						scale_sz = scale,
						public=form['choices']=='publico',
						user=request.user)
			file_db.save()
			msg = 'Archivo %s subido exitosamente.' % (the_file.name)
	data = {'form':UploadForm(initial={'choices':'privado'}),
			'msg':msg}
	return render(request,'upload_file.html',data)

def download_file(request,file_id):
	the_file = get_object_or_404(File,id=file_id,public=True)
	if request.method == 'GET' and 'download' in request.GET and request.GET['download'] == 'yes':
		wrapper = FileWrapper(file(the_file.filepath))
		mimetype = mimetypes.guess_type(the_file.filepath)[0]
		if not mimetype:
			mimetype = "octet-stream"
		response = HttpResponse(wrapper, content_type='application/'+mimetype)
		response['Content-Length'] = the_file.real_size
		response['Content-Disposition'] = "attachment; filename=%s" % the_file.filename
		return response
	return render(request,'download_file.html',{'file':the_file})

@login_required
def swap_public(request):
	if request.method == "POST":
		file_id = request.POST['file_id']
		the_file = get_object_or_404(File,id=file_id)
		if the_file.user.id != request.user.id:
			return JsonResponse({'msg': "You don't own this file!"}, status=403)
		the_file.public = not the_file.public
		estado = 'Público' if the_file.public else 'Privado'
		the_file.save()
		data = {
			'estado':estado,
			'publicado':the_file.public,
			'share_url':request.build_absolute_uri(reverse('download_file', args=(the_file.id,)))
		}
		return JsonResponse(data)
	raise Http404

@login_required
def delete_file(request,file_id):
	the_file = get_object_or_404(File,id=file_id)
	if the_file.user.id != request.user.id:
		return render(request, 'forbidden.html', status=403)
	if request.method == 'POST':
		os.remove(the_file.filepath)
		the_file.delete()
		return redirect('show_files')
	return render(request,'delete_file.html',{'file':the_file})

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			already_exists = (
				User.objects.filter(username=data['username']).count() != 0)
			if already_exists:
				form.add_error('username', 'El nombre de usuario ya existe.')
				return render(request, 'register.html', {'form': form}, status=409)
			User.objects.create_user(
				data['username'],
				data['email'],
				data['password'],
				first_name=data['first_name'],
				last_name=data['last_name'])
			return redirect('home')
		else:
			return render(request, 'register.html', {'form': form}, status=422)
	return render(request, 'register.html', {'form': RegisterForm()})
