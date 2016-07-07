from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404
#from django.utils.decorators import method_decorator

from django.views.generic import CreateView, ListView


from .models import Photo


class PhotoCreate(CreateView):
    model = Photo
    fields = ('title', 'content', 'image', )
    template_name = 'create_photo.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(PhotoCreate, self).form_valid(form)


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


class PhotoList(ListView):
    model = Photo
    context_object_name = 'photos'
    template_name = 'list_photos.html'


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
