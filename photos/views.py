from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse


from .models import Photo
from .forms import PhotoForm


@login_required
def create_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST)

        if form.is_vaild() is True:
            new_photo = form.save(commit=False)
            new_photo = request.user
            new_photo.save()

            redirect('photos:view_photo', kwargs={'pk':new_photo.pk})
    else:
        return render(request, 'create_photo.html')


def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    if photo.user != request.user:
        raise PermissionDenied

    photo.delete()

    return redirect(reverse('photos:list_photos'))



def view_photo(request, pk):
    photo = Photo.objects.get(pk=pk)

    context = {
        'photo': photo,
    }

    return render(request, 'view_photo.html', context)



def list_photos(request):
    photos = Photo.objects.all()

    context = {
        'photos': photos,
    }

    return render(request, 'list_photos.html', context)


def create_comment(request, pk):
    pass


def delete_comment(request, pk):
    pass
