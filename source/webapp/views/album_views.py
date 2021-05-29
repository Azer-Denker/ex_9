from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse, reverse_lazy

from webapp.models import Album, Photo
from webapp.forms import AlbumForm


class IndexView(ListView):
    model = Album
    template_name = 'album/index.html'
    ordering = ['created_at']
    paginate_by = 5
    context_object_name = 'albums'


class AlbumView(DetailView):
    model = Album
    template_name = 'album/album_view.html'
    paginate_photos_by = 5
    paginate_photos_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        photos, page, is_paginated = self.paginate_photos(self.object)
        context['photos'] = photos
        context['page_obj'] = page
        context['is_paginated'] = is_paginated

        return context

    def paginate_photos(self, album):
        photos = album.photo_album.all().order_by('-created_at')
        if photos.count() > 0:
            paginator = Paginator(photos, self.paginate_photos_by, orphans=self.paginate_photos_orphans)
            page_number = self.request.GET.get('page', 1)
            page = paginator.get_page(page_number)
            is_paginated = paginator.num_pages > 1
            return page.object_list, page, is_paginated
        else:
            return photos, None, False


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'album/album_create.html'

    def get_success_url(self):
        return reverse('webapp:album_view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        album = form.save(commit=False)
        album.author = self.request.user
        album.save()
        return redirect('webapp:album_view', pk=album.pk)


class AlbumUpdateView(PermissionRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'album/album_update.html'
    permission_required = 'webapp.change_album'

    def has_permission(self):
        album = self.get_object()
        return super().has_permission() or album.author == self.request.user

    def get_success_url(self):
        return reverse('webapp:album_view', kwargs={'pk': self.object.pk})


class AlbumDeleteView(PermissionRequiredMixin, DeleteView):
    model = Album
    template_name = 'album/album_delete.html'
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_album'

    def has_permission(self):
        album = self.get_object()
        return super().has_permission() or album.author == self.request.user
