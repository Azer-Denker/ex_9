from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse, reverse_lazy

from webapp.models import Photo
from webapp.forms import PhotoForm


class PIndexView(ListView):
    model = Photo
    template_name = 'photos/index.html'
    ordering = ['created_at']
    paginate_by = 5
    context_object_name = 'photos'


class PhotoView(DetailView):
    model = Photo
    template_name = 'photos/photo_view.html'

    def get_context_data(self, **kwargs):
        photo = get_object_or_404(Photo, pk=self.object.pk)
        users_which_like = photo.favorite_photo.all()
        kwargs['likes'] = users_which_like
        return super().get_context_data(**kwargs)


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/photo_create.html'

    def get_success_url(self):
        return reverse('webapp:photo_view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.author = self.request.user
        photo.save()
        return redirect('webapp:photo_view', pk=photo.pk)


class PhotoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/photo_update.html'
    permission_required = 'webapp.change_photo'

    def has_permission(self):
        photo = self.get_object()
        return super().has_permission() or photo.author == self.request.user

    def get_success_url(self):
        return reverse('webapp:photo_view', kwargs={'pk': self.object.pk})


class PhotoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photos/photo_delete.html'
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_photo'

    def has_permission(self):
        photo = self.get_object()
        return super().has_permission() or photo.author == self.request.user
