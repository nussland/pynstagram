from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


from .models import Photo


class PhotoCreate(CreateView):
    model = Photo
    fields = ('title', 'content', 'image', )
    template_name = 'create_photo.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(PhotoCreate, self).form_valid(form)


class PhotoDelete(DeleteView):
    model = Photo
    template_name = 'delete_photo.html'
    context_object_name = 'photo'
    success_url = reverse_lazy('photos:list_photos')

    def get_object(self, queryset=None):
        obj = super(PhotoDelete, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


class PhotoView(DetailView):
    model = Photo
    template_name = 'view_photo.html'

    def get_context_data(self, **kwargs):
        context = super(PhotoView, self).get_context_data(**kwargs)
        return context


class PhotoList(ListView):
    model = Photo
    context_object_name = 'photos'
    template_name = 'list_photos.html'

