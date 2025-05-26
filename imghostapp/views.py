from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import ImageForm
from django.contrib import messages
from .models import Image
from account.models import Account
from django.http import HttpResponseForbidden, FileResponse, Http404
from imghostapp.utils.storage import get_user_storage_size, get_user_storage_limit
from django.views.generic import ListView
import os

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
               uploaded_file = request.FILES['image']
               uploaded_file_size = uploaded_file.size
               current_usage = get_user_storage_size(request.user)
               max_limit = get_user_storage_limit(request.user)
          
               if current_usage + uploaded_file_size > max_limit:
                    messages.error(request, 'Upload failed: Storage limit exceeded.')
                    return redirect('upload-image')
    
               try:
                    image.save()
                    messages.success(request, 'Image has been uploaded to the server')
               except Exception as e:
                    messages.error(request, f'Error saving image: {str(e)}')
                    return redirect('upload-image')

     else:
               form = ImageForm()
    
     return render(request, 'imghostapp/upload.html', {'form': form})

@login_required
def download_image(request, image_id):
     try:
          image = Image.objects.get(pk=image_id)
          file_path = image.image.path
          if image.user != request.user and not (request.user.is_admin or request.user.is_staff or request.user.is_superuser):
               raise Http404('You cannot access this file')
          return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
     except Image.DoesNotExist:
          raise Http404("This file does not exist")
     except FileNotFoundError:
          raise Http404("File has not been found")


class UserGalleryView(ListView):
    model = Image
    template_name = 'gallery/user_gallery.html'
    context_object_name = 'images'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.user_profile = get_object_or_404(Account, username=kwargs['username'])

        if request.user != self.user_profile and not (
            request.user.is_authenticated and (
                request.user.is_admin or request.user.is_staff or request.user.is_superuser
            )
        ):
            return HttpResponseForbidden("Sorry, you can't access this site.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Image.objects.filter(user=self.user_profile).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_usage = get_user_storage_size(self.user_profile)
        max_limit = get_user_storage_limit(self.user_profile)
        context.update({
            'user': self.user_profile,
            'current_usage': current_usage,
            'max_limit': max_limit,
            'remaining_space': max_limit - current_usage,
        })
        return context


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
          return HttpResponseForbidden("You are not allowed to edit this image")
     if request.method == 'POST':
          new_title = request.POST.get('title')
          if new_title:
               image.title = new_title
               image.save()
               return redirect('user_gallery', username=request.user.username)
     return render(request, 'gallery/edit_image.html', {'image':image})