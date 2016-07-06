from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


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
    pass



def view_photo(request, pk):
    photo = Photo.objects.get(pk=pk)

    context = {
        'photo': photo,
    }

    return render(request, 'view_photo.html', context)



def list_photos(request):
    pass


def create_comment(request, pk):
    pass


def delete_comment(request, pk):
    pass
