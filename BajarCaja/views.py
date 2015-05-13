from django.shortcuts import render
from BajarCaja.models import File

def home(request):
	return render(request,'BajarCaja/home.html',{})

def view_files(request):
	latest_files = File.objects.order_by('-upload_date')[:5]
	context ={'latest_files': latest_files,}
	return render(request,'BajarCaja/view_files.html',context)

def upload_file(request):
	if request.POST:
		
	else:
		return render(request,'BajarCaja/upload_file.html',{})
	