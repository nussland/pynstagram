from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic.edit import CreateView


from .models import Photo
from .forms import PhotoForm


class PhotoCreate(CreateView):
    model = Photo
    fields = ('title', 'content', )
    template_name = 'create_photo.html'

    def form_valid(self, form):
        new_photo = form.save(commit=False)
        new_photo.user = self.request.user
        new_photo.save()
        return super(PhotoCreate, self).form_valid(form)

create_photo = login_required(PhotoCreate.as_view())


@login_required
def delete_photo(request, pk):
    if request.method == 'POST':
        photo = get_object_or_404(Photo, pk=pk)

        if photo.user != request.user:
            raise PermissionDenied

        photo.delete()

        return redirect(reverse('photos:list_photos'))
    else:
        return HttpResponse()

def view_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

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
