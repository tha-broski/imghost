from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import ImageForm
from django.contrib import messages
from .models import Image
from account.models import Account
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator

# Create your views here.
def home_view(request):
	context = {}
	return render(request, "imghostapp/home.html", context)

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            messages.success(request, 'Image has been uploaded to the server')
            return redirect('upload-image')
    else:
        form = ImageForm()
    
    return render(request, 'imghostapp/upload.html', {'form': form})

def user_gallery(request, username):
     user = get_object_or_404(Account, username=username)

     if request.user != user and not (
          request.user.is_authenticated and (
               request.user.is_admin or request.user.is_staff or request.user.is_superuser
          )
        ):
          return HttpResponseForbidden("Sorry, you can't access this site.")
     
     images_list = Image.objects.filter(user=user).order_by('-created_at')

     # Paginator
     paginator = Paginator(images, 10)
     page_number = request.GET.get('page')
     images = paginator.get_page(page_number)

     return render(request, 'gallery/user_gallery.html', {'user':user, 'images':images})

@login_required
def delete_image(request, image_id):
     image = get_object_or_404(Image, id=image_id)
     if request.user == image.user or request.user.is_staff or request.user.is_superuser:
          image.delete()
     return redirect('user_gallery', username=request.user.username)

@login_required
def edit_image(request, image_id):
     image = get_object_or_404(Image, id=image_id)
     if request.user != image.user:
          return HttpResponseForbidden
     if request.method == 'POST':
          new_title = request.POST.get('title')
          if new_title:
               image.title = new_title
               image.save()
               return redirect('user_gallery', username=request.user.username)
     return render(request, 'gallery/edit_image.html', {'image':image})