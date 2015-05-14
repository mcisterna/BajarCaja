# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse, Http404
from BajarCaja.models import File
from forms import UploadForm
from django.conf import settings
from datetime import datetime
from django.core.servers.basehttp import FileWrapper
import mimetypes,os

def home(request):
	return render(request,'home.html',{})

def show_files(request):
	latest_files = File.objects.order_by('-upload_date')
	context ={'latest_files': latest_files,}
	return render(request,'show_files.html',context)

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
						public=form['choices']=='publico')
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

def swap_public(request):
	if request.method == "POST":
		file_id = request.POST['file_id']
		the_file = get_object_or_404(File,id=file_id)
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

def delete_file(request,file_id):
	the_file = get_object_or_404(File,id=file_id)
	if request.method == 'POST':
		os.remove(the_file.filepath)
		the_file.delete()
		return redirect('show_files')
	return render(request,'delete_file.html',{'file':the_file})
	